"""
:copyright: (c) 2016 Jiakun Jin
email: jiakun@kth.se
:license: LGPL?
"""
from Stream_Detector import Stream_Detector
import ctypes

__author__ = 'jiakun'

class DDM(Stream_Detector):
    def __init__(self,threshold = 1,alpha = 2.0, beta = 3.0 ):
        '''
        This is the stream detector using DDM algorithm
        :param threshold: When the score exceeds the threshold then the prob of anomalous increases
        :return:
        '''
        Stream_Detector.__init__(self)
        self.Detector = ctypes.CDLL("./Stream_AnomalyDetector/C++/DDM.so")
        self.Detector.Process.argtypes = [ctypes.c_double]
        self.Detector.init.argtypes = [ctypes.c_double,ctypes.c_double,ctypes.c_double]
        self.Detector.init(threshold,alpha,beta)


    def check(self,score):
        '''
        Check whether an anomalous happens for the incoming score
        :param score: The incoming score
        :return: Whether a drift detected
        '''
        Stream_Detector.check(self)
        return self.Detector.Process(score)