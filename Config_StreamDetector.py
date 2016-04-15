"""
:copyright: (c) 2016 Jiakun Jin
email: jiakun@kth.se
:license: LGPL?
"""
from Stream_AnomalyDetector.DDM import DDM
from Stream_AnomalyDetector.CUSUM import CUSUM

__author__ = 'jiakun'

def DDM_StreamDetector(threshold=1):
    '''

    :param threshold:
    :return:
    '''
    return DDM(threshold)


def CUSUM_StreamDetector(drift = 1, threshold = 1):
    '''

    :param drift:
    :param threshold:
    :return:
    '''
    return CUSUM(drift,threshold)



