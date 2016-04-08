from Stream_AnomalyDetector.DDM import DDM
from Stream_AnomalyDetector.CUSUM import CUSUM


def DDM_StreamDetector(threshold=1):
    return DDM(threshold)


def CUSUM_StreamDetector(drift = 1, threshold = 1):
    return CUSUM(drift,threshold)



