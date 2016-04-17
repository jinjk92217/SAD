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

    :param threshold: When the score exceeds the threshold then the prob of anomalous increases
    e.g. 3.0
    :return:
    '''
    return DDM(threshold)


def CUSUM_StreamDetector(drift = 1, threshold = 1):
    '''

    :param drift: The drift of the score that could be detected
    e.g. 1.0
    :param threshold: the threshold that during some period the positive and negative changes exceeds the threshold
    e.g. 10.0
    :return:

    '''
    return CUSUM(drift,threshold)



