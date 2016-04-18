"""
:copyright: (c) 2016 Jiakun Jin
email: jiakun@kth.se
:license: LGPL?
"""

from AnomalyScorer import AnomalyScorer
import pyisc
import numpy as np
from lof import LOF
from sklearn.neighbors.unsupervised import NearestNeighbors

__author__ = 'jiakun'

class LOFAnomalyScorer(AnomalyScorer):
    def __init__(self,n_neighbors=10,algorithm = 'auto'):
        '''
        This is the point detector using lof algorithm
        This by default needs the training phase
        :param n_neighbors: number of the neighbors
        :param algorithm: which algorithms to use, default auto
        :return:
        '''
        AnomalyScorer.__init__(self)
        self.n_neighbors = n_neighbors
        self.algorithm = algorithm
        return

    def Train_PointDetector(self,data):
        '''
        For training the point detector
        :param data: the input for training the point detector
        :return:
        '''
        AnomalyScorer.Train_PointDetector(self)
        return self._lof(data)

    def _lof(self,data):
        '''

        :param data: the input for training the lof algorithm
        :return:
        '''
        nbrs = NearestNeighbors(n_neighbors=self.n_neighbors, algorithm=self.algorithm).fit(data)
        #nbrs.kneighbors([[0, 0, 1.3,1,2,3]], 2, return_distance=False)
        #print(nbrs.predict([[-1.1,-1.1]]))
        self.lof = LOF(nbrs)
        self.lof.anomaly_score_training_data()
        #return lof
    def anomaly_score(self,data):
        AnomalyScorer.anomaly_score(self)
        return self.lof.anomaly_score(data)

    def fit_incrementally(self,data):
        AnomalyScorer.fit_incrementally(self)
        return self.lof.fit_incrementally(data)