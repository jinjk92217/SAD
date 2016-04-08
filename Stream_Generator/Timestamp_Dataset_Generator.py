from Generator import Generator
import numpy as np
from sklearn.cross_validation import train_test_split
import random
from scipy.stats import poisson,norm
import csv

class Timestamp_Dataset_Generator(Generator):
    def __init__(self,filename,delimiter=",",del_timestamp_column=True,timestamp_column=0):
        Generator.__init__(self)
        self.attribute = []
        self.data_set = []
        self._read_datafile(filename,delimiter,del_timestamp_column,timestamp_column)
        # self.data_set = self._addclass(self.data_set)
        self.train = []
        self.test = self.data_set
        self.currentpoint = 0

    def Generate_TrainData(self,percentage):
        Generator.Generate_TrainData(self)
        #self._read_datafile(filename,delimiter,normal_class,column)
        self._Train_point(percentage)
        #print self.train.__len__()
        return np.hstack([self.train])



    def Generate_Stream(self,type="Normal",number=1):
        Generator.Generate_Stream(self)
        self.currentpoint = self.currentpoint + number
        # print self.currentpoint,len(self.test)
        if self.currentpoint >=len(self.test):
            return []
        return np.hstack(self.test[self.currentpoint - number])


    def _read_datafile(self,filename,delimiter,del_timestamp_column=True,timestamp_column=0):
            with open(filename, 'r') as f:
                read_data = f.read().splitlines()
                row_number = 0
                for row in read_data:
                    words = row.split(delimiter)
                    if row_number ==0:
                        row_number = 1
                        continue
                    if del_timestamp_column ==True:
                        words.__delitem__(timestamp_column)
                        words = [float(x) for x in words]
                        self.data_set.append(words)
            # print self.data_set


    def _Train_point(self,perceptage):
        #global train,test
        self.train, self.test = self.data_set[:int(perceptage*len(self.data_set))],self.data_set[int(perceptage*len(self.data_set)):]


    def _Generate_error_sudden(self,number):
        Generator._Generate_error_sudden(self)




    def _Generate_error_outlier(self,number):
        Generator._Generate_error_outlier(self)



    def _Generate_error_gradual(self,number):
        Generator._Generate_error_gradual(self)
