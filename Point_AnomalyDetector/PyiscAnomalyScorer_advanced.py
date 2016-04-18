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

class PyiscAnomalyScorer_advanced(AnomalyScorer):
    def __init__(self,dist = ['norm']):
        '''
        This is the point detector from pyisc framework
        There is training phase which will fit the data in distributions in dist and also poisson
        :param dist: the distributions for pyisc which wants to be tried, see distributions in Fit_data
        :return:
        '''
        AnomalyScorer.__init__(self)
        self.Fit_data = Fit_data()
        self.test_distribution = dist
        return

    def Train_PointDetector(self,data):
        '''

        :param data: The data which is used for training
        :return:
        '''
        AnomalyScorer.Train_PointDetector(self)
        return self._PYISC(data)


    def _PYISC(self,data):
        '''

        :param data: the training data
        :return:
        '''
        models= []
        #print data[:,0]
        #print Counter(data[:,1]).most_common(1)[0][1]
        # print "shaper",data.shape[1]
        flag = -1
        for i in range(0,data.shape[1]):
            if Counter(data[:,i]).most_common(1)[0][1]> 0.99 * data.shape[0] and flag ==-1 and data.shape[1]>1:
                # print "aaaaa"
                flag = i
                continue
            models.append([i,self.Fit_data.find_distribution(data[:,i],test_distribution=self.test_distribution)[0]])
        component_models = []
        for x in models:
            # print x
            if x[1] == 'poisson' and flag >=0:
                component_models.append(pyisc.P_Poisson(x[0],flag))
            #elif x[1] == 'norm':
            else:
                component_models.append(pyisc.P_Gaussian(x[0]))
            # elif x[1] == 'poisson':
            #     component_models.append(pyisc.P_Poisson(x[0],0))
        # print "aaaaaaaaaaaaaaaaaaaa",component_models,
        self.anomaly_detector = pyisc.AnomalyDetector(
            component_models=component_models,
            output_combination_rule=pyisc.cr_max
        )
        self.anomaly_detector.fit(data)
        #scores = anomaly_detector.anomaly_score(data)
        #print scores[-15:]
        #return anomaly_detector
    def anomaly_score(self,data):
        AnomalyScorer.anomaly_score(self)
        return self.anomaly_detector.anomaly_score(data)

    def fit_incrementally(self,data):
        AnomalyScorer.fit_incrementally(self)
        return self.anomaly_detector.fit_incrementally(data)