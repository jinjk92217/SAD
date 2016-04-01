from AnomalyScorer import AnomalyScorer
from collections import Counter
import pyisc
import numpy as np
from Fit_data import Fit_data
class PyiscAnomalyScorer(AnomalyScorer):
    def __init__(self):
        AnomalyScorer.__init__(self)
        self.Fit_data = Fit_data()
        return

    def Train_PointDetector(self,data):
        AnomalyScorer.Train_PointDetector(self)
        return self._PYISC(data)


    def _PYISC(self,data):
        models= []
        #print data[:,0]
        #print Counter(data[:,1]).most_common(1)[0][1]
        #print "shaper",data.shape[1]
        for i in range(0,data.shape[1]):
            if Counter(data[:,i]).most_common(1)[0][1]> 0.9 * data.shape[0]:
                continue
            models.append([i,self.Fit_data.find_distribution(data[:,i])[0]])
        component_models = []
        for x in models:
            #print x[1]
            if x[1] == 'norm':
                component_models.append(pyisc.P_Gaussian(x[0]))
            elif x[1] == 'poisson':
                component_models.append(pyisc.P_Poisson(x[0],0))
        anomaly_detector = pyisc.AnomalyDetector(
            component_models=component_models,
            output_combination_rule=pyisc.cr_max
        )
        anomaly_detector.fit(data)
        #scores = anomaly_detector.anomaly_score(data)
        #print scores[-15:]
        return anomaly_detector