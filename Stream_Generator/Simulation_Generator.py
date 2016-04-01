from Generator import Generator
import numpy as np
class Simulation_Generator(Generator):
    def __init__(self,list_distribution,normal_error_distribution,anomaly_error_distribution):
        Generator.__init__(self)
        self.list_distribution = list_distribution
        self.normal_error_distribution = normal_error_distribution
        self.anomaly_error_distribution = anomaly_error_distribution

    def Generate_TrainData(self,number,first=1):
        Generator.Generate_TrainData(self)
        return np.column_stack(
                    self._generate_matrix(self.list_distribution,number,first)
                )

    def Generate_Stream(self,type_error,number):
        Generator.Generate_Stream(self)
        if type_error == "Normal":
            #print number
            #print self._Generate_error(number,0,self.normal_error_distribution)
            return self.Generate_TrainData(number,1)+ self._Generate_error_sudden(number,0,self.normal_error_distribution)
        elif type_error == "Sudden":
            return self.Generate_TrainData(number,1)+ self._Generate_error_sudden(number,0,self.anomaly_error_distribution)
        elif type_error == "Gradual":
            return self.Generate_TrainData(number,1)+ self._Generate_error_gradual(number,0,self.anomaly_error_distribution)
        elif type_error == "Outlier":
            return self.Generate_TrainData(10,1)+ self._Generate_error_outlier(10,0,self.anomaly_error_distribution)

    def _generate_matrix(self,list_dist,number,first):
            #self.list_distribution = list_dist
            #print self.list_distribution
            data = [[first]*number]
            for x in list_dist:
                data.append(list(x.rvs(number)))
            return data


    def _Generate_error_sudden(self,number,first,distribution):
        Generator._Generate_error_sudden(self)
        return np.column_stack(
                       self._generate_matrix([distribution]*len(self.list_distribution),number,0)
        )


    def _Generate_error_outlier(self,number,first,distribution):
        Generator._Generate_error_outlier(self)
        return np.column_stack(
                       self._generate_matrix([distribution]*len(self.list_distribution),number,0)
        )


    def _Generate_error_gradual(self,number,first,distribution):
        Generator._Generate_error_gradual(self)
        k = number / 20
        stream = []
        for i in range(0,5):
            if i == 0:
                stream = np.row_stack((np.column_stack(
                       self._generate_matrix([self.normal_error_distribution]*len(self.list_distribution),k,0)),
                    np.column_stack(
                       self._generate_matrix([distribution]*len(self.list_distribution),k*(i+1),0)
                )))
                #print stream
            else:
                stream = np.row_stack((stream,np.column_stack(
                       self._generate_matrix([self.normal_error_distribution]*len(self.list_distribution),k,0)),
                    np.column_stack(
                       self._generate_matrix([distribution]*len(self.list_distribution),k*(i+1),0)
                )))
        stream = np.row_stack((stream, np.column_stack(
                       self._generate_matrix([distribution]*len(self.list_distribution),number - k*20,0)
                )))
        return stream