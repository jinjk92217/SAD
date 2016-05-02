from Stream_Detector import Stream_Detector
import ctypes


class PRAAG(Stream_Detector):
    def __init__(self, r = 100,  l = 1000,  e = 0.0001,  a = 14.0, k=0.05):
        Stream_Detector.__init__(self)
        self.Detector = ctypes.CDLL("./Stream_AnomalyDetector/C++/PRAAG.so")
        self.Detector.Process.argtypes = [ctypes.c_double]
        self.Detector.init.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double]
        # tag: return A
        self.Detector.Process.restype = ctypes.POINTER(ctypes.c_double)
        self.Detector.init(r,l,e,a, k)


    def check(self,score):
        Stream_Detector.check(self)
        return self.Detector.Process(score)