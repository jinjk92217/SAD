from AnomalyScorer import AnomalyScorer
import pyisc
import numpy as np
from lof import LOF
from sklearn.neighbors.unsupervised import NearestNeighbors
class LOFAnomalyScorer(AnomalyScorer):
    def __init__(self,n_neighbors=10,algorithm = 'auto'):
        AnomalyScorer.__init__(self)
        self.n_neighbors = n_neighbors
        self.algorithm = algorithm
        return

    def Train_PointDetector(self,data):
        AnomalyScorer.Train_PointDetector(self)
        return self._lof(data)

    def _lof(self,data):
        nbrs = NearestNeighbors(n_neighbors=self.n_neighbors, algorithm=self.algorithm).fit(data)
        #nbrs.kneighbors([[0, 0, 1.3,1,2,3]], 2, return_distance=False)
        #print(nbrs.predict([[-1.1,-1.1]]))
        lof = LOF(nbrs)
        lof.anomaly_score_training_data()
        return lof