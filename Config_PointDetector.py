from Point_AnomalyDetector.PyiscAnomalyScorer import PyiscAnomalyScorer
from Point_AnomalyDetector.PyiscAnomalyScorer_advanced import PyiscAnomalyScorer_advanced
from Point_AnomalyDetector.LOFAnomalyScorer import LOFAnomalyScorer



def pyisc_PointDetector(train_data=[],models=[],incremental=False,test_distribution=['norm']):
    if incremental==False:

        Point_Detector = PyiscAnomalyScorer_advanced(dist=test_distribution)
    else:
        train_data = []
        Point_Detector = PyiscAnomalyScorer(
        models=models
    )
    #if incremental == False:
    return Point_Detector.Train_PointDetector(train_data)



def lof_PointDetector(train_data=[],n_neighbors = 10, algorithm='auto'):
    Point_Detector = LOFAnomalyScorer(n_neighbors, algorithm)
    return Point_Detector.Train_PointDetector(train_data)