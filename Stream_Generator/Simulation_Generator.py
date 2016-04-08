from Generator import Generator
import numpy as np
class Simulation_Generator(Generator):
    def __init__(self,list_distribution,normal_error_distribution,anomaly_error_distribution,type_error="Sudden"):
        Generator.__init__(self,type_error)
        self.list_distribution = list_distribution
        self.normal_error_distribution = normal_error_distribution
        self.anomaly_error_distribution = anomaly_error_distribution

    def Generate_TrainData(self,number):
        # Generator.Generate_TrainData(self)
        # return self._addclass(np.column_stack(
        #             self._generate_matrix(self.list_distribution,number)
        #         ))
       return np.column_stack(
                    self._generate_matrix(self.list_distribution,number)
                )



    def _Generate_StreamData(self,number):
        #Generator.Generate_TrainData(self)
        return np.column_stack(
                    self._generate_matrix(self.list_distribution,number)
                )
    # def Generate_Stream(self,type,number):
    #     Generator.Generate_Stream(self)
    #     # return self._addclass(self._Generate_Stream(type,number))
    #     return self._Generate_Stream(type,number)

    def Generate_Stream(self,type,number):
        Generator.Generate_Stream(self)
        if type == "Normal":
            #print number
            #print self._Generate_error(number,0,self.normal_error_distribution)
            if self.type_error == "Sudden":
                return self._Generate_StreamData(number)+ self._Generate_error_sudden(number,self.normal_error_distribution)
            elif self.type_error =="Gradual":
                return self._Generate_StreamData(number)+ self._Generate_error_gradual(number,self.normal_error_distribution)
            elif self.type_error =="Outlier":
                return self._Generate_StreamData(number)+ self._Generate_error_outlier(number,self.normal_error_distribution)
            return self._Generate_StreamData(number)+ self._Generate_error_sudden(number,self.normal_error_distribution)
        #print "type_error",self.type_error
        elif self.type_error == "Sudden":
            return self._Generate_StreamData(number)+ self._Generate_error_sudden(number,self.anomaly_error_distribution)
        elif self.type_error == "Gradual":
            return self._Generate_StreamData(number)+ self._Generate_error_gradual(number,self.anomaly_error_distribution)
        elif self.type_error == "Outlier":
            return self._Generate_StreamData(10)+ self._Generate_error_outlier(10,self.anomaly_error_distribution)

    def _generate_matrix(self,list_dist,number):
            #self.list_distribution = list_dist
            #print self.list_distribution
            data = []
            for x in list_dist:
                if isinstance(x,int) or isinstance(x,float):
                    data.append([x]*number)
                    continue
                try:
                    data.append(list(x.rvs(number)))
                except Exception as e:
                    print e
            return data


    def _Generate_error_sudden(self,number,distribution):
        Generator._Generate_error_sudden(self)
        return np.column_stack(
                       self._generate_matrix(distribution,number)
        )


    def _Generate_error_outlier(self,number,distribution):
        Generator._Generate_error_outlier(self)
        return np.column_stack(
                       self._generate_matrix(distribution,number)
        )


    def _Generate_error_gradual(self,number,distribution):
        Generator._Generate_error_gradual(self)
        k = number / 20
        stream = []
        for i in range(0,5):
            if i == 0:
                stream = np.row_stack((np.column_stack(
                       self._generate_matrix(self.normal_error_distribution,k)),
                    np.column_stack(
                       self._generate_matrix(distribution,k*(i+1))
                )))
                #print stream
            else:
                stream = np.row_stack((stream,np.column_stack(
                       self._generate_matrix(self.normal_error_distribution,k)),
                    np.column_stack(
                       self._generate_matrix(distribution,k*(i+1))
                )))
        stream = np.row_stack((stream, np.column_stack(
                       self._generate_matrix(distribution,number - k*20)
                )))
        return stream