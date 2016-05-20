"""
:copyright: (c) 2016 Jiakun Jin
email: jiakun@kth.se
:license: LGPL?
"""
from Stream_Detector import Stream_Detector
import ctypes

__author__ = 'jiakun'

class FCWM(Stream_Detector):
    def __init__(self,number_bin = 100,ref_size=10000,rec_size=1000,maxn=20.0, update_able=1, Lambda=1.0 ):
        '''
        This is the stream detector using DDM algorithm
        :param threshold: When the score exceeds the threshold then the prob of anomalous increases
        :return:
        '''
        Stream_Detector.__init__(self)
        self.Detector = ctypes.CDLL("./Stream_AnomalyDetector/C++/FCWM.so")
        self.Detector.Process.argtypes = [ctypes.c_double]
        self.Detector.init.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_double,ctypes.c_bool,ctypes.c_double]
        self.Detector.init(number_bin,ref_size,rec_size,maxn, update_able, Lambda)


    def check(self,score):
        '''
        Check whether an anomalous happens for the incoming score
        :param score: The incoming score
        :return: Whether a drift detected
        '''
        Stream_Detector.check(self)
        if score == float('inf'):
            return self.Detector.Process(99999999)
        return self.Detector.Process(score)