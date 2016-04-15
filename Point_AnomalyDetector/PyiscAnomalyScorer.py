"""
:copyright: (c) 2016 Jiakun Jin
email: jiakun@kth.se
:license: LGPL?
"""
from AnomalyScorer import AnomalyScorer
from collections import Counter
import pyisc
import numpy as np
from Fit_data import Fit_data

__author__ = 'jiakun'

class PyiscAnomalyScorer(AnomalyScorer):
    def __init__(self,models= []):
        '''
        This is the point detector using pyisc framework
        There is no training phase for this framework, all the distributions are in models
        :param models: input the component models for pyisc, useful for the incremental implementation
        :return:
        '''
        AnomalyScorer.__init__(self)
        self.Fit_data = Fit_data()
        self.component_models = models
        return

    def Train_PointDetector(self,data=[]):
        '''

        :param data: train the point detector according to the data
        :return:
        '''
        AnomalyScorer.Train_PointDetector(self)
        return self._PYISC(data)


    def _PYISC(self,data):
        '''

        :param data: the training data for pyisc
        :return:
        '''
        anomaly_detector = pyisc.AnomalyDetector(
            component_models=self.component_models,
            output_combination_rule=pyisc.cr_max
        )
        if data!=[]:
            anomaly_detector.fit(data)
        #scores = anomaly_detector.anomaly_score(data)
        #print scores[-15:]
        return anomaly_detector