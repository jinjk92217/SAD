"""
:copyright: (c) 2016 Jiakun Jin
email: jiakun@kth.se
:license: LGPL?
"""
import numpy as np

__author__ = 'jiakun'

class Generator(object):
    def __init__(self,type_error="Sudden"):
        '''
        The super class of the Generator
        :param type_error:Type of the errors generated in the simulation and datastamp data, it's not useful for the timestamp
        :return:
        '''
        #self.error_distribution = error_distribution
        self.type_error = type_error
        pass

    def Generate_TrainData(self):
        '''
        This is the super interface for generating training data
        Using this method it could generate training data which is used for not incremental test
        :return:
        '''
        pass

    def Generate_Stream(self,number=0):
        '''
        This is the super interface for generating stream data
        :param number:number of data from stream
        :return:
        '''
        pass

    def _Generate_error_sudden(self):
        '''
        This is the super interface for generating sudden error stream
        Only for simulation and dataset generator
        :param
        :return:
        '''
        pass


    def _Generate_error_outlier(self):
        '''
        This is the super interface for generating outlier error stream
        Only for simulation and dataset generator
        :param
        :return:
        '''
        pass

    def _Generate_error_gradual(self):
        '''
        This is the super interface for generating gradual error stream
        Only for simulation and dataset generator
        :param
        :return:
        '''
        pass


    # def _addclass(self,data):
    #     return np.column_stack((
    #                 [1]*len(data),data
    #             ))