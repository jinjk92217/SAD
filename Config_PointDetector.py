"""
:copyright: (c) 2016 Jiakun Jin
email: jiakun@kth.se
:license: LGPL?
"""
from Point_AnomalyDetector.PyiscAnomalyScorer import PyiscAnomalyScorer
from Point_AnomalyDetector.PyiscAnomalyScorer_advanced import PyiscAnomalyScorer_advanced
from Point_AnomalyDetector.LOFAnomalyScorer import LOFAnomalyScorer

__author__ = 'jiakun'

def pyisc_PointDetector(train_data=[],models=[],incremental=False,test_distribution=['norm']):
    '''

    :param train_data: The training data for the pyisc point detector, they are in matrix format
    :param models: The models used for incremental detection,
    e.g. [pyisc.P_Gaussian(1),pyisc.P_Gaussian(2),pyisc.P_Poisson(3,0),pyisc.P_Poisson(4,0)]
    :param incremental: Whether they are training incremental or not
    :param test_distribution: If there is training phase, the test_distribution is the list used for testing the best distribution
    e.g.['norm']
    :return:
    '''
    if incremental==False:

        Point_Detector = PyiscAnomalyScorer_advanced(dist=test_distribution)
    else:
        train_data = []
        Point_Detector = PyiscAnomalyScorer(
        models=models
    )
    #if incremental == False:
    Point_Detector.Train_PointDetector(train_data)
    return Point_Detector



def lof_PointDetector(train_data=[],n_neighbors = 10, algorithm='auto'):
    '''

    :param train_data:
    :param n_neighbors:
    :param algorithm:
    :return:
    '''
    Point_Detector = LOFAnomalyScorer(n_neighbors, algorithm)
    Point_Detector.Train_PointDetector(train_data)
    return Point_Detector