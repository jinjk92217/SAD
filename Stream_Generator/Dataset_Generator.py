"""
:copyright: (c) 2016 Jiakun Jin
email: jiakun@kth.se
:license: LGPL?
"""
from Generator import Generator
import numpy as np
from sklearn.cross_validation import train_test_split

__author__ = 'jiakun'

class Dataset_Generator(Generator):
    def __init__(self,filename,delimiter=",",normal_class="value",column=-1,type_error = "Sudden"):
        '''
        For generating the stream data from data_set
        If the need training phase, also used for generating train_data
        For stream data, they could generate errors from type_error
        :param filename: the filename for the data set
        :param delimiter: the delimiter in the data set
        :param normal_class: the normal class of the data set
        :param column: the column for the feature
        :param type_error: the type of the error
        :return:
        '''
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
        '''

        :param percentage: if in not incremental mode, the percentage is the training percentage
        :return:
        '''
        Generator.Generate_TrainData(self)
        #self._read_datafile(filename,delimiter,normal_class,column)
        self._Train_point(percentage)
        #print self.train.__len__()
        return np.hstack([self.train])



    def Generate_Stream(self,type,number):
        '''
        :param type: type is either normal or anomaly
        :param number: number of the stream data generated
        :return: the matrix of the stream data according to the distribution and type
        '''
        Generator.Generate_Stream(self)
        #self._UpdateSeed()
        if type == "Normal":
                #stream = np.hstack([random.sample(list, 5)])
            #print np.hstack([random.sample(self.test,10)])
            return np.hstack([self.ran.sample(self.test,number>len(self.test) and len(self.test) or number)])
            #return self.test[random.randint(0,len(self.test)-1)]
        #print np.hstack([random.sample(self.Anormal_data_set,number>len(self.test) and len(self.test) or number)])

        elif self.type_error =="Sudden":
            return self._Generate_error_sudden(number)

        elif self.type_error =="Outlier":
            return self._Generate_error_outlier(10)
        elif self.type_error == "Gradual":
            return self._Generate_error_gradual(number)
        elif self.type_error == "Incremental":
            return self._Generate_error_incremental(number)
        #return self.Anormal_data_set[random.randint(0,len(self.Anormal_data_set)-1)]





    def _read_datafile(self,filename,delimiter,normal_class,column=-1):
        '''

        :param filename: the filename of the data set you read from
        :param delimiter: the delimiter of the column
        :param normal_class: the normal class selected
        :param column: the column of the attribution chosen
        :return:
        '''
        #self._UpdateSeed()
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
        '''
        :param perceptage: seprate the data into training and testing data
        :return:
        '''
        #self._UpdateSeed()
        #global train,test
        self.train, self.test = train_test_split(self.Normal_data_set, test_size = perceptage,random_state = self.ran.randint(0,4294967295))




    def _Generate_error_sudden(self,number):
        '''

        :param list_dist: generate the stream cases
        :param number: the number of the stream cases
        :return: matrix
        '''
        Generator._Generate_error_sudden(self)
        #self._UpdateSeed()
        return np.hstack([self.ran.sample(self.Anormal_data_set,number>len(self.test) and len(self.test) or number)])

    def _Generate_error_incremental(self,number):
        '''

        :param list_dist: generate the stream cases
        :param number: the number of the stream cases
        :return: matrix
        '''
        Generator._Generate_error_incremental(self)
        return self._Generate_error_gradual(number)

    def _Generate_error_outlier(self,number):
        '''

        :param list_dist: generate the stream cases
        :param number: the number of the stream cases
        :return: matrix
        '''
        Generator._Generate_error_outlier(self)
        #self._UpdateSeed()
        return np.hstack([self.ran.sample(self.Anormal_data_set,number>len(self.test) and len(self.test) or number)])


    def _Generate_error_gradual(self,number):
        '''

        :param list_dist: generate the stream cases
        :param number: the number of the stream cases
        :return: matrix
        '''
        Generator._Generate_error_gradual(self)
        #self._UpdateSeed()
        k = number / 20
        stream = []
        for i in range(0,5):
            if i == 0:
                stream = np.row_stack((np.hstack([self.ran.sample(self.test,k>len(self.test) and len(self.test) or k)]),
                    np.hstack([self.ran.sample(self.Anormal_data_set,k>len(self.test) and len(self.test) or k)])))
                #print stream
            else:
                stream = np.row_stack((stream,np.hstack([self.ran.sample(self.test,k>len(self.test) and len(self.test) or k)]),
                    np.hstack([self.ran.sample(self.Anormal_data_set,k*(i+1)>len(self.test) and len(self.test) or k*(i+1))])))
        stream = np.row_stack((stream,  np.hstack([self.ran.sample(self.Anormal_data_set,number - k*20>len(self.test) and len(self.test) or number - k*20)])))
        return stream