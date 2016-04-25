"""
:copyright: (c) 2016 Jiakun Jin
:license: LGPL?
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager
from sklearn import svm
from AnomalyScorer import AnomalyScorer

__author__ = 'jiakun'

class SVMAnomalyScorer(AnomalyScorer):
    def __init__(self, nu = 0.1, kernel = "rbf", gamma = 0.1, coefficient = 1.5):
        '''
        Class One_Class_SVM implements the Local Outlier Factor algorithm,
        This will use one_class SVM.
        more implementations, see
        http://scikit-learn.org/stable/modules/generated/sklearn.svm.OneClassSVM.html#sklearn.svm.OneClassSVM
        :param nu: An upper bound on the fraction of training errors and a lower bound of the fraction of support vectors
        :param kernel:Specifies the kernel type to be used in the algorithm.It must be one of "linear", "poly", "rbf", "sigmoid", "precomputed" or a callable.
        :param gamma:Kernel coefficient for "poly", "rbf", "sigmoid". If gamma is "auto" then 1/n_features will be used instead.
        :param coefficient:For calculating the score, we return the 1.0/exp(distance to the boundary), however the distances are toolarge, we need to adjust the distances in order to get good anomaly scores
        :return:
        '''
        self.clf = svm.OneClassSVM(nu=nu, kernel=kernel, gamma=gamma)
        self.coefficient = coefficient

    def Train_PointDetector(self,data=[]):
        '''

        :param data: train the point detector according to the data
        :return:
        '''
        AnomalyScorer.Train_PointDetector(self)
        return self._anomaly_score_training_data(data)

    def anomaly_score(self, X_test, in_training_set=False):
        '''
        :param X: an array containing data to score
        :param in_training_set: a boolean that indicates whether the scored data set is present in the training data set.
        :return: an anomly score for each data point in X
        '''
        self.tmpscore = 1.0/np.exp(self.clf.decision_function(X_test)/self.coefficient)
        if self.tmpscore[0][0]>20:
            return np.matrix([20])
        return self.tmpscore
        return 1.0/np.exp(self.clf.decision_function(X_test)/self.coefficient)

    def _anomaly_score_training_data(self,X_train):
        self.clf.fit(X_train)

    def fit_incrementally(self,data):
        AnomalyScorer.fit_incrementally(self)
        return self.anomaly_detector.fit_incrementally(data)
