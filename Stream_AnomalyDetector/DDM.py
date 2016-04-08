from Stream_Detector import Stream_Detector
import ctypes


class DDM(Stream_Detector):
    def __init__(self,threshold = 1):
        Stream_Detector.__init__(self)
        self.Detector = ctypes.CDLL("./Stream_AnomalyDetector/C++/DDM.so")
        self.Detector.Process.argtypes = [ctypes.c_double]
        self.Detector.init.argtypes = [ctypes.c_double]
        self.Detector.init(threshold)


    def check(self,score):
        Stream_Detector.check(self)
        return self.Detector.Process(score)