"""
:copyright: (c) 2016 Jiakun Jin
email: jiakun@kth.se
:license: LGPL?
"""
from Generator import Generator
import numpy as np
from sklearn.cross_validation import train_test_split
import random
from scipy.stats import poisson,norm
import csv


__author__ = 'jiakun'

class Timestamp_Dataset_Generator(Generator):
    def __init__(self,filename,delimiter=",",del_timestamp_column=True,timestamp_column=0):
        '''
        For generating the timestamp stream
        If the need training phase, also used for generating train_data
        For stream data, they generate time series stream
        :param filename: The filename of the data set
        :param delimiter: the delimiter in the data set
        :param del_timestamp_column: whether to delete the timestamp column
        :param timestamp_column: the timestamp_column which you dont want to use
        :return:
        '''
        Generator.__init__(self)
        self.attribute = []
        self.data_set = []
        self._read_datafile(filename,delimiter,del_timestamp_column,timestamp_column)
        # self.data_set = self._addclass(self.data_set)
        self.train = []
        self.test = self.data_set
        self.currentpoint = 0

    def Generate_TrainData(self,percentage):
        '''

        :param percentage: the percentage for training the data, only useful in not incremental method
        :return:
        '''
        Generator.Generate_TrainData(self)
        #self._read_datafile(filename,delimiter,normal_class,column)
        self._Train_point(percentage)
        #print self.train.__len__()
        return np.hstack([self.train])



    def Generate_Stream(self,type="Normal",number=1):
        '''

        :param type: normal or anomaly, however it's useless here
        :param number: number of the stream, however it's useless here
        :return:
        '''
        Generator.Generate_Stream(self)
        self.currentpoint = self.currentpoint + number
        # print self.currentpoint,len(self.test)
        if self.currentpoint >=len(self.test):
            return []
        return np.hstack(self.test[self.currentpoint - number])


    def _read_datafile(self,filename,delimiter,del_timestamp_column=True,timestamp_column=0):
        '''

        :param filename: the filename
        :param delimiter: the delimiter in the file
        :param del_timestamp_column: whether to delete the timestamp column
        :param timestamp_column: the column in the data set
        :return:
        '''
        with open(filename, 'r') as f:
            read_data = f.read().splitlines()
            row_number = 0
            for row in read_data:
                words = row.split(delimiter)
                if row_number ==0:
                    row_number = 1
                    continue
                if del_timestamp_column ==True:
                    words.__delitem__(timestamp_column)
                    words = [float(x) for x in words]
                    self.data_set.append(words)
        # print self.data_set


    def _Train_point(self,perceptage):
        '''

        :param perceptage: the percentage to train the data set, useless in incremental mode
        :return:
        '''
        #global train,test
        self.train, self.test = self.data_set[:int(perceptage*len(self.data_set))],self.data_set[int(perceptage*len(self.data_set)):]


    def _Generate_error_sudden(self,number):
        Generator._Generate_error_sudden(self)




    def _Generate_error_outlier(self,number):
        Generator._Generate_error_outlier(self)



    def _Generate_error_gradual(self,number):
        Generator._Generate_error_gradual(self)
