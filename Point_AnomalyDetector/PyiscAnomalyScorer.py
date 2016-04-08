from AnomalyScorer import AnomalyScorer
from collections import Counter
import pyisc
import numpy as np
from Fit_data import Fit_data
class PyiscAnomalyScorer(AnomalyScorer):
    def __init__(self,models= []):
        AnomalyScorer.__init__(self)
        self.Fit_data = Fit_data()
        self.component_models = models
        return

    def Train_PointDetector(self,data=[]):
        AnomalyScorer.Train_PointDetector(self)
        return self._PYISC(data)


    def _PYISC(self,data):
        anomaly_detector = pyisc.AnomalyDetector(
            component_models=self.component_models,
            output_combination_rule=pyisc.cr_max
        )
        if data!=[]:
            anomaly_detector.fit(data)
        #scores = anomaly_detector.anomaly_score(data)
        #print scores[-15:]
        return anomaly_detector