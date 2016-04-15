"""
:copyright: (c) 2016 Jiakun Jin
email: jiakun@kth.se
:license: LGPL?
"""
from Stream_Detector import Stream_Detector
import ctypes

__author__ = 'jiakun'

class CUSUM(Stream_Detector):
    def __init__(self,drift = 1, threshold = 1):
        '''
        This the stream detector using CUSUM algorithm
        :param drift: The drift of the score that could be detected
        :param threshold: the threshold that during some period the positive and negative changes exceeds the threshold
        :return:
        '''
        Stream_Detector.__init__(self)
        self.Detector = ctypes.CDLL("./Stream_AnomalyDetector/C++/CUSUM.so")
        self.Detector.Process.argtypes = [ctypes.c_double]
        self.Detector.init.argtypes = [ctypes.c_double, ctypes.c_double]
        self.Detector.init(drift,threshold)


    def check(self,score):
        '''
        Check whether an anomalous happens for the incoming score
        :param score: The incoming score
        :return: Whether a drift detected
        '''
        Stream_Detector.check(self)
        return self.Detector.Process(score)