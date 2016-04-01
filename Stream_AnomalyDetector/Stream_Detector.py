import ctypes

class Stream_Detector(object):
    def __init__(self,filepath,parameters):
        self.Stream_Detector = ctypes.CDLL("./Stream_AnomalyDetector/C++/"+filepath)
        self.Stream_Detector.Process.argtypes = [ctypes.c_double]
        #print [ctypes.c_double] * len(parameters)
        #self.Stream_Detector.init.argtypes = [ctypes.c_double] * len(parameters)
        #Array = ctypes.c_double * parameters
        arr = (ctypes.c_double * len(parameters))(*parameters)
        #print Array(arr)
        self.Stream_Detector.init(arr)
        return

    def classifier(self,score):
        return self.Stream_Detector.Process(score)