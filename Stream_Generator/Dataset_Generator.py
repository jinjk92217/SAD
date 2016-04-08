from Generator import Generator
import numpy as np
from sklearn.cross_validation import train_test_split
import random
from scipy.stats import poisson,norm


class Dataset_Generator(Generator):
    def __init__(self,filename,delimiter=",",normal_class="value",column=-1,type_error = "Sudden"):
        Generator.__init__(self,type_error)
        self.attribute = []
        self.Normal_data_set = []
        self.Anormal_data_set = []

        self._read_datafile(filename,delimiter,normal_class,column)
        # self.Normal_data_set = self._addclass(self.Normal_data_set)
        # self.Anormal_data_set = self._addclass(self.Anormal_data_set)
        self.train = []
        self.test = self.Normal_data_set

    def Generate_TrainData(self,percentage):
        Generator.Generate_TrainData(self)
        #self._read_datafile(filename,delimiter,normal_class,column)
        self._Train_point(percentage)
        #print self.train.__len__()
        return np.hstack([self.train])



    def Generate_Stream(self,type,number):
        Generator.Generate_Stream(self)
        if type == "Normal":
                #stream = np.hstack([random.sample(list, 5)])
            #print np.hstack([random.sample(self.test,10)])
            return np.hstack([random.sample(self.test,number>len(self.test) and len(self.test) or number)])
            #return self.test[random.randint(0,len(self.test)-1)]
        #print np.hstack([random.sample(self.Anormal_data_set,number>len(self.test) and len(self.test) or number)])

        elif self.type_error =="Sudden":
            return self._Generate_error_sudden(number)

        elif self.type_error =="Outlier":
            return self._Generate_error_outlier(10)
        elif self.type_error == "Gradual":
            return self._Generate_error_gradual(number)
        #return self.Anormal_data_set[random.randint(0,len(self.Anormal_data_set)-1)]





    def _read_datafile(self,filename,delimiter,normal_class,column=-1):
            with open(filename, 'r') as f:
                read_data = f.read().splitlines()
                for row in read_data:
                    words = row.split(delimiter)
                    if words[column]==normal_class:
                        words.__delitem__(column)
                        words = [float(x) for x in words]
                        self.Normal_data_set.append(words)
                    else:
                        words.__delitem__(column)
                        words = [float(x) for x in words]
                        self.Anormal_data_set.append(words)


    def _Train_point(self,perceptage):
            #global train,test
            self.train, self.test = train_test_split(self.Normal_data_set, test_size = perceptage)




    def _Generate_error_sudden(self,number):
        Generator._Generate_error_sudden(self)
        return np.hstack([random.sample(self.Anormal_data_set,number>len(self.test) and len(self.test) or number)])



    def _Generate_error_outlier(self,number):
        Generator._Generate_error_outlier(self)
        return np.hstack([random.sample(self.Anormal_data_set,number>len(self.test) and len(self.test) or number)])


    def _Generate_error_gradual(self,number):
        Generator._Generate_error_gradual(self)
        k = number / 20
        stream = []
        for i in range(0,5):
            if i == 0:
                stream = np.row_stack((np.hstack([random.sample(self.test,k>len(self.test) and len(self.test) or k)]),
                    np.hstack([random.sample(self.Anormal_data_set,k>len(self.test) and len(self.test) or k)])))
                #print stream
            else:
                stream = np.row_stack((stream,np.hstack([random.sample(self.test,k>len(self.test) and len(self.test) or k)]),
                    np.hstack([random.sample(self.Anormal_data_set,k*(i+1)>len(self.test) and len(self.test) or k*(i+1))])))
        stream = np.row_stack((stream,  np.hstack([random.sample(self.Anormal_data_set,number - k*20>len(self.test) and len(self.test) or number - k*20)])))
        return stream