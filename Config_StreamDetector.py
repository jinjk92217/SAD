"""
:copyright: (c) 2016 Jiakun Jin
email: jiakun@kth.se
:license: LGPL?
"""
from Stream_AnomalyDetector.DDM import DDM
from Stream_AnomalyDetector.FCWM import FCWM
from Stream_AnomalyDetector.CUSUM import CUSUM
from Stream_AnomalyDetector.PRAAG import PRAAG

__author__ = 'jiakun'

def DDM_StreamDetector(threshold=1,alpha = 2.0, beta = 3.0 ):
    '''

    :param threshold: When the score exceeds the threshold then the prob of anomalous increases
    e.g. 3.0
    :return:
    '''
    return DDM(threshold,alpha,beta)


def CUSUM_StreamDetector(drift = 1, threshold = 1):
    '''

    :param drift: The drift of the score that could be detected
    e.g. 1.0
    :param threshold: the threshold that during some period the positive and negative changes exceeds the threshold
    e.g. 10.0
    :return:

    '''
    return CUSUM(drift,threshold)


def FCWM_StreamDetector(number_bin = 100,ref_size=10000,rec_size=1000,maxn=20.0, update_able=1, Lambda=1.0 ):
    '''

    :param drift: The drift of the score that could be detected
    e.g. 1.0
    :param threshold: the threshold that during some period the positive and negative changes exceeds the threshold
    e.g. 10.0
    :return:

    '''
    return FCWM(number_bin,ref_size,rec_size,maxn, update_able, Lambda)


def PRAAG_StreamDetector(r = 100,  l = 1000,  e = 0.0001,  a = 15, k=0.05):
    '''

    :param r: Size of recent window(small one)
    :param l: Size of reference window(large one)
    :param e: precision, needed only if using GK quantile estimation
    :param a: thresthold of negative log probability value
    :param k: thresthold percentage of considering a window abnormal
    :return:

    '''
    return PRAAG(r,l,e,a,k)



