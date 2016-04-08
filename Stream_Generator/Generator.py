import numpy as np
class Generator(object):
    def __init__(self,type_error="Sudden"):
        #self.error_distribution = error_distribution
        self.type_error = type_error
        pass

    def Generate_TrainData(self):
        pass

    def Generate_Stream(self,type_error="Normal",number=0):
        pass

    def _Generate_error_sudden(self):
        pass


    def _Generate_error_outlier(self):
        pass

    def _Generate_error_gradual(self):
        pass


    # def _addclass(self,data):
    #     return np.column_stack((
    #                 [1]*len(data),data
    #             ))