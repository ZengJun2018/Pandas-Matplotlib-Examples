# -*- coding: utf-8 -*-
# -*- Environment: Python 3.6  Tensorflow 1.12: -*-
"""
Created on Tue Feb 12 2019
@author: Wang Wei
Updated1 on Tue Mar 05 2019
@author: Wang Wei
Updated2 on Tue Mar 12 2019
@author: Wang Wei
Updated3 on Thu Mar 14 2019
@author: Wang Wei
Updated4 on TUE Mar 26 2019
@author: Wang Wei
Updated5 on SAT Mar 30 2019
@author: Wang Wei
"""
"""
Purpose:
Spindle failure prediction, including system unblance failure and bearing failure.
Note:
A buffer is used to receive kafka data.
"""

import time
import numpy as np
import pandas as pd
from scipy.fftpack import fft

import dynamic_ylim
import myplot

class Spindle():
    # preprocess: initialization
    def __init__(self):
        self.init_sampling()
        self.init_filter()
        self.init_write_file()
        self.init_data_array()

    # sampling initialization
    def init_sampling(self):
        self.SAMPLING_RATE = 25000
        # sensor's sampling rate
        self.UNIT_CONVERSION_RATIO = 2.5
        # unit conversion ratio to converse orignal acceleration data to unit of mg (g: gravitational acceleration - 9.80665 m/s2)
        self.SAMPLING_LENGTH = 4.2  # 4.2 = 0.028 * 5 * 3 * 7
        # unit: second  # sampling length needed to make a prediction
        self.SAMPLING_POINT = int(self.SAMPLING_RATE * self.SAMPLING_LENGTH)
        # number of points needed for failure prediction : 105,000
        self.SLICE_LENGTH = 1.4     # 1.4 = 0.028 * 5 * 10
        # unit: second  # failure prediction interval
        self.SLICE_POINT = int(self.SAMPLING_RATE * self.SLICE_LENGTH)
        # number of points in failure prediction interval : 35000
        self.PACKAGE_LENGTH = 0.14  # 0.14 = 0.028 * 5
        # unit: second  # package received from kafka interval
        self.PACKAGE_POINT = int(self.SAMPLING_RATE * self.PACKAGE_LENGTH)   # 700 * 5 = 3500
        # number of points of package from kafka
        self.SAMPLING_SLICE_RATIO = int(self.SAMPLING_POINT / self.SLICE_POINT)
        # samping slice ratio is 3
        self.SLICE_PACKAGE_RATIO = int(self.SLICE_POINT / self.PACKAGE_POINT)
        # slice package ratio is 10

    # filter initialization
    def init_filter(self):
        self.UNBLANCE_FILTER = (50, 90)
        self.INNER_FILTER = (800, 1500)
        self.OUTER_FILTER = (600, 1300)
        self.BALL_FILTER = (200, 700)
        self.CAGE_FILTER = (10, 60)
        # filter range of difference failure

    # local file path of data writing
    def init_write_file(self):
        self.WRITE_FOLDER_PATH = r'E:\data'
        self.WRITE_FILE_NAME = r'data-' + time.strftime('%Y%m%d_%H%M%S', time.localtime())  # mark file name by time
        # self.WRITE_FILE_NAME = r'XXXXX'   # for customed file name
        self.WRITE_FILE = self.WRITE_FOLDER_PATH + '\\' + self.WRITE_FILE_NAME + '.' + 'csv'
        # path of data file for writing

    # bulid adat array to store data from kafka and use them for spindle failure prediction
    def init_data_array(self):
        self.data = np.zeros((self.SAMPLING_SLICE_RATIO, self.SLICE_PACKAGE_RATIO, self.PACKAGE_POINT))
        self.row = 0
        self.column = 0
        # work like poniter

    # receive data from kafka
    def kafka_receive(self, kafka_dict):
        kafka_data = np.array(kafka_dict['data'])
        # extract data from kafka dict
        self.data[self.row][self.column] = kafka_data * self.UNIT_CONVERSION_RATIO
        self.column += 1
        if self.column == self.SLICE_PACKAGE_RATIO:
            # a row is full and it's time to make prediction NOW！
            self.failure_prediction()
            # failure prediction GO GO GO!!!
            self.row = (self.row + 1) % self.SAMPLING_SLICE_RATIO
            # move to next row and go back to top if it reach the end
            self.column = 0
            return 1 # finish prediction
        else:
            return 0 # still need more data to predict

    # send data to kafka
    def kafka_send_pred(self):
        return self.prediction_dict
        # dict of prediction result

    # send fundamental frequency peak data
    def kafka_send_FF(self):
        return self.FF_frequency, self.FF_amplitude
        # frequency and amplitude of fundamental frequency peak

    # spindle failure prediction
    def failure_prediction(self):
        self.data_FFT() # FFT to calculate spectrum
        unblance_prediction_dict = self.unblance_prediction(self.UNBLANCE_FILTER)
        # spindle unblance prediction
        inner_prediction_dict = self.inner_prediction(self.INNER_FILTER)
        outer_prediction_dict = self.outer_prediction(self.OUTER_FILTER)
        ball_prediction_dict = self.ball_prediction(self.BALL_FILTER)
        cage_prediction_dict = self.cage_prediction(self.CAGE_FILTER)
        # spindle bearing prediction
        self.prediction_dict = unblance_prediction_dict.copy()
        self.prediction_dict.update(inner_prediction_dict)
        self.prediction_dict.update(outer_prediction_dict)
        self.prediction_dict.update(ball_prediction_dict)
        self.prediction_dict.update(cage_prediction_dict)
        # merge prediction result together in a new dict
        ''' data written in local file '''
        writer = pd.DataFrame(self.data[self.row].reshape(1,-1))
        writer.to_csv(self.WRITE_FILE, index=0, header=0, mode='a')
        ''' data written in local file '''
        ''' data plot for debugger '''
        # myplot.plot_unblance(self.prediction_dict)
        # myplot.plot_bearing(self.prediction_dict)
        ''' data plot for debugger '''

    # data reading and FFT
    def data_FFT(self):
        temp = np.zeros_like(self.data)
        # temp array to store time domain data for FFT
        for i in range(self.SAMPLING_SLICE_RATIO):
            temp[i] = self.data[(self.row + 1 + i) % self.SAMPLING_SLICE_RATIO]
        temp = temp.reshape(-1)
        # rebuild time domain array sequentially
        self.spectrum = abs(fft(temp)) / self.SAMPLING_POINT * 2
        "!!Attention!!:" # amplitude after FFT is divide by point number
        "!!Attention!!:" # only half of spectrum will be used (due to symmetry of frequency spectrum)

    # spindle unblance prediction
    def unblance_prediction(self, filter):
        unblance_x = np.arange(self.limit_to_frequency(filter[0]), self.limit_to_frequency(filter[1]), 1/self.SAMPLING_LENGTH)
        unblance_y = self.spectrum[self.limit_to_index(filter[0]) : self.limit_to_index(filter[1])]
        # calculate x,y array by filter limit
        self.FF_frequency, self.FF_amplitude = self.peak_analysis(unblance_x, unblance_y)
        unblance_pred = self.unblance_prediction_classification(self.FF_frequency, self.FF_amplitude)
        # spindle unblance prediction by a trained machine learning module
        unblance_x_show = unblance_x
        unblance_y_show = unblance_y
        # data to plot and show in UI
        unblance_x_lim = filter
        unblance_y_lim = (0, dynamic_ylim.unblance_ylim(self.FF_frequency * 60))
        # x,y axis range (y axis is dynamic)
        unblance_prediction_dict = {
            'rpm' : self.FF_frequency * 60,
            'unblance_pred' : unblance_pred,
            'unblance_x' : tuple(unblance_x_show),
            'unblance_y' : tuple(unblance_y_show),
            'unblance_x_lim' : unblance_x_lim,
            'unblance_y_lim' : unblance_y_lim
        }
        return unblance_prediction_dict

    def inner_prediction(self, filter):
        inner_x = np.arange(self.limit_to_frequency(filter[0]), self.limit_to_frequency(filter[1]), 1/self.SAMPLING_LENGTH)
        inner_y = self.spectrum[self.limit_to_index(filter[0]) : self.limit_to_index(filter[1])]
        # calculate x,y array by filter limit
        inner_pred = 0
        inner_health = 0.98
        # failure prediction and health analysis (undone)
        inner_x_show = self.data_compress_frequency(inner_x, 10)
        inner_y_show = self.data_compress_amplitude(inner_y, 10)
        # data compresssion to plot
        inner_x_lim = filter
        inner_y_lim = (0, 25)
        # x,y axis range
        inner_prediction_dict = {
            'inner_pred' : inner_pred,
            'inner_health' : inner_health,
            'inner_x' : tuple(inner_x_show),
            'inner_y' : tuple(inner_y_show),
            'inner_x_lim' : inner_x_lim,
            'inner_y_lim' : inner_y_lim
        }
        return inner_prediction_dict

    def outer_prediction(self, filter):
        outer_x = np.arange(self.limit_to_frequency(filter[0]), self.limit_to_frequency(filter[1]), 1/self.SAMPLING_LENGTH)
        outer_y = self.spectrum[self.limit_to_index(filter[0]) : self.limit_to_index(filter[1])]
        # calculate x,y array by filter limit
        outer_pred = 0
        outer_health = 0.98
        # failure prediction and health analysis (undone)
        outer_x_show = self.data_compress_frequency(outer_x, 10)
        outer_y_show = self.data_compress_amplitude(outer_y, 10)
        # data compresssion to plot
        outer_x_lim = filter
        outer_y_lim = (0, 25)
        # x,y axis range
        outer_prediction_dict = {
            'outer_pred' : outer_pred,
            'outer_health' : outer_health,
            'outer_x' : tuple(outer_x_show),
            'outer_y' : tuple(outer_y_show),
            'outer_x_lim' : outer_x_lim,
            'outer_y_lim' : outer_y_lim
        }
        return outer_prediction_dict

    def ball_prediction(self, filter):
        ball_x = np.arange(self.limit_to_frequency(filter[0]), self.limit_to_frequency(filter[1]), 1/self.SAMPLING_LENGTH)
        ball_y = self.spectrum[self.limit_to_index(filter[0]) : self.limit_to_index(filter[1])]
        # calculate x,y array by filter limit
        ball_pred = 0
        ball_health = 1.0
        # failure prediction and health analysis (undone)
        ball_x_show = self.data_compress_frequency(ball_x, 8)
        ball_y_show = self.data_compress_amplitude(ball_y, 8)
        # data compresssion to plot
        ball_x_lim = filter
        ball_y_lim = (0, 15)
        # x,y axis range
        ball_prediction_dict = {
            'ball_pred' : ball_pred,
            'ball_health' : ball_health,
            'ball_x' : tuple(ball_x_show),
            'ball_y' : tuple(ball_y_show),
            'ball_x_lim' : ball_x_lim,
            'ball_y_lim' : ball_y_lim
        }
        return ball_prediction_dict

    def cage_prediction(self, filter):
        cage_x = np.arange(self.limit_to_frequency(filter[0]), self.limit_to_frequency(filter[1]), 1/self.SAMPLING_LENGTH)
        cage_y = self.spectrum[self.limit_to_index(filter[0]) : self.limit_to_index(filter[1])]
        # calculate x,y array by filter limit
        cage_pred = 0
        cage_health = 0.90
        # failure prediction and health analysis (undone)
        cage_x_show = cage_x
        cage_y_show = cage_y
        # data compresssion to plot
        cage_x_lim = filter
        cage_y_lim = (0, 15)
        # x,y axis range
        cage_prediction_dict = {
            'cage_pred' : cage_pred,
            'cage_health' : cage_health,
            'cage_x' : tuple(cage_x_show),
            'cage_y' : tuple(cage_y_show),
            'cage_x_lim' : cage_x_lim,
            'cage_y_lim' : cage_y_lim
        }
        return cage_prediction_dict

    # search peak amplitude and peak frequency from frequency spectrum
    def peak_analysis(self, x, y):  # x is frequency axis, y is amplitude axis
        peak_frequency = 0
        peak_amplitude = 0
        for i in range(x.shape[0]):
            if y[i] > peak_amplitude:
                peak_frequency = x[i]
                peak_amplitude = y[i]
        # seach peak amplitude and frequency
        if peak_amplitude < 5:
            peak_frequency = 0
        # avoid noise interference
        return (float(peak_frequency), float(peak_amplitude))

    # spindle unblance prediction
    def unblance_prediction_classification(self, FF_frequency, FF_amplitude):
        ylim = dynamic_ylim.unblance_ylim(FF_frequency*60)
        if FF_amplitude < 0.6 * ylim:
            return 0 # balance is OK
        else:
            return 1 # unblance!

    # calculate index in data array by filter limit (y axis)
    def limit_to_index(self, limit):
        return int(limit * self.SAMPLING_LENGTH)
        # index must be int

    # calculate frequency by filter limit (x axis)
    def limit_to_frequency(self, limit):
        return self.limit_to_index(limit) / self.SAMPLING_LENGTH
        # converse to int index first, then calculate frequency refer to index

    # decrease data size to plot (too many points may be difficult for UI to plot)
    def data_compress_frequency(self, data_in, ratio):
        # 'data_in' is original data numpy array; ratio is compresssion ratio
        size_out = int(data_in.shape[0] / ratio)
        data_out = np.zeros(size_out)
        # data_out initialization
        for i in range(size_out):
            data_out[i] = data_in[i*ratio : (i+1)*ratio].sum() / ratio
        # data compresssion method: average value
        return  data_out

    # decrease data size to plot (too many points may be difficult for UI to plot)
    def data_compress_amplitude(self, data_in, ratio):
        # 'data_in' is original data numpy array; ratio is compresssion ratio
        size_out = int(data_in.shape[0] / ratio)
        data_out = np.zeros(size_out)
        # data_out initialization
        for i in range(size_out):
            data_out[i] = data_in[i*ratio : (i+1)*ratio].max() 
        # data compresssion method: max value
        data_out -= data_out.min()
        # eliminate bias when using max value method (compromise plan)
        return  data_out
