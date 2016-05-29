"""
:copyright: (c) 2016 Jiakun Jin
email: jiakun@kth.se
:license: LGPL?
"""
from Generator import Generator
import numpy as np

__author__ = 'jiakun'

class Simulation_Generator(Generator):
    def __init__(self,list_distribution,normal_error_distribution,anomaly_error_distribution,type_error="Sudden"):
        '''
        For generating the siulation stream data, the features are in list_distributions
        If the need training phase, also used for generating train_data
        For stream data, they could generate errors from type_error
        :param list_distribution: the distribution type for normal cases
        :param normal_error_distribution:the error distribution types for normal cases
        :param anomaly_error_distribution:the error distribution types for anomaly cases
        :param type_error: the error type for the stream
        :return:
        '''
        Generator.__init__(self,type_error)
        self.list_distribution = list_distribution
        self.normal_error_distribution = normal_error_distribution
        self.anomaly_error_distribution = anomaly_error_distribution

    def Generate_TrainData(self,number):
        '''
        :param number: number of the data generated for training
        :return: the matrix of the training data according to the distribution
        '''
        return np.column_stack(
                    self._generate_matrix(self.list_distribution,number)
        )
        # Generator.Generate_TrainData(self)
        # return self._addclass(np.column_stack(
        #             self._generate_matrix(self.list_distribution,number)
        #         ))





    def _Generate_StreamData(self,number):
        '''
        :param number: number of the stream data generated
        :return: the matrix of the stream data according to the distribution
        '''
        #Generator.Generate_TrainData(self)
        return np.column_stack(
                    self._generate_matrix(self.list_distribution,number)
                )
    # def Generate_Stream(self,type,number):
    #     Generator.Generate_Stream(self)
    #     # return self._addclass(self._Generate_Stream(type,number))
    #     return self._Generate_Stream(type,number)

    def Generate_Stream(self,type,number):
        '''
        :param type: type is either normal or anomaly
        :param number: number of the stream data generated
        :return: the matrix of the stream data according to the distribution and type
        '''
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
            elif self.type_error =="Incremental":
                return self._Generate_StreamData(number)+ self._Generate_error_incremental(number,self.normal_error_distribution)
            return self._Generate_StreamData(number)+ self._Generate_error_sudden(number,self.normal_error_distribution)
        #print "type_error",self.type_error
        elif self.type_error == "Sudden":
            return self._Generate_StreamData(number)+ self._Generate_error_sudden(number,self.anomaly_error_distribution)
        elif self.type_error == "Gradual":
            return self._Generate_StreamData(number)+ self._Generate_error_gradual(number,self.anomaly_error_distribution)
        elif self.type_error == "Outlier":
            return self._Generate_StreamData(50)+ self._Generate_error_outlier(50,self.anomaly_error_distribution)
        elif self.type_error == "Incremental":
            return self._Generate_StreamData(number)+ self._Generate_error_incremental(number,self.anomaly_error_distribution)

    def _generate_matrix(self,list_dist,number):
        '''

        :param list_dist: generate the stream cases
        :param number: the number of the stream cases
        :return: matrix
        '''
        #self.list_distribution = list_dist
        #print self.list_distribution
        #self._UpdateSeed()
        data = []
        for x in list_dist:
            if isinstance(x,int) or isinstance(x,float):
                data.append([x]*number)
                continue
            try:
                #self._UpdateSeed()
                data.append(list(x.rvs(number,random_state=self.ran.randint(0,4294967295))))
            except Exception as e:
                print e
        return data


    def _Generate_error_sudden(self,number,distribution):
        '''

        :param list_dist: generate the stream cases
        :param number: the number of the stream cases
        :return: matrix
        '''
        Generator._Generate_error_sudden(self)
        return np.column_stack(
                       self._generate_matrix(distribution,number)
        )

    def _Generate_error_incremental(self,number,distribution):
        '''

        :param list_dist: generate the stream cases
        :param number: the number of the stream cases
        :return: matrix
        '''
        Generator._Generate_error_incremental(self)
        stream = 1.0  / 3 *np.column_stack(
                       self._generate_matrix(distribution,number / 3))
        for i in range(2,3):
            stream = np.row_stack((stream, 1.0 * i / 3 *np.column_stack(
                       self._generate_matrix(distribution,number / 3))))
        stream = np.row_stack((stream, np.column_stack(self._generate_matrix(distribution,number - number / 3 * 2))))
        return stream


    def _Generate_error_outlier(self,number,distribution):
        '''

        :param list_dist: generate the stream cases
        :param number: the number of the stream cases
        :return: matrix
        '''
        Generator._Generate_error_outlier(self)
        return np.column_stack(
                       self._generate_matrix(distribution,number)
        )


    def _Generate_error_gradual(self,number,distribution):
        '''

        :param list_dist: generate the stream cases
        :param number: the number of the stream cases
        :return: matrix
        '''
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