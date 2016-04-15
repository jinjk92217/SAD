"""
:copyright: (c) 2016 Jiakun Jin
email: jiakun@kth.se
:license: LGPL?
"""



import ctypes

__author__ = 'jiakun'

class Stream_Detector(object):
    def __init__(self,para = 0.0):
        '''
        This is the super class for Stream_detector
        :param para:
        :return:
        '''

        pass
        #self.Detector.Process.argtypes = [ctypes.c_double]
        #print [ctypes.c_double] * len(parameters)
        #self.Stream_Detector.init.argtypes = [ctypes.c_double] * len(parameters)
        #Array = ctypes.c_double * parameters
        #arr = (ctypes.c_double * len(parameters))(*parameters)
        #print Array(arr)
        #self.Detector.init(arr)

    def check(self,score = 0.0):
        '''
        This is for checking whether there is anomalous happening when a new score comes
        :param score: The score from the point detector
        :return:
        '''
        pass
        #return self.Detector.Process(score)