"""
:copyright: (c) 2016 Jiakun Jin
email: jiakun@kth.se
:license: LGPL?
"""
from Stream_Generator.Simulation_Generator import Simulation_Generator
from Stream_Generator.Dataset_Generator import Dataset_Generator
from scipy.stats import poisson,norm
from Stream_Generator.Timestamp_Dataset_Generator import Timestamp_Dataset_Generator


__author__ = 'jiakun'

def Generate_from_simulation(Normal_Error,Anomaly_Error,list_distribution,type_error,incremental=False,Number_Of_Train=10000):
    '''
    This is functions for generating simulation data
    :param Normal_Error: The error distributions added for normal cases
    e.g. [0,poisson(1.0),poisson(1.0),poisson(1.0),poisson(1.0)]
    :param Anomaly_Error: The error distributions added for anomaly cases
    e.g.[0,poisson(1.0),poisson(1.0),poisson(10.0),poisson(1.0)]
    :param list_distribution: The distributions used for cases
    e.g.[1,norm(5,12),norm(10,20),poisson(10),poisson(100)]
    :param type_error: The type of errors generated in simulation cases
    e.g."Sudden" or "Gradual" or "Outlier"
    :param incremental: If the incremental is true,then no need training data, else, need training data
    :param Number_Of_Train: if incremental is true, no usage, else, the simulation cases for training data
    :return:
    '''
     #simulation data setup

    #Configure the Normal_error or Anomaly_error distribution
    #Normal_Error = [poisson(1.0),poisson(1.0),poisson(1.0),poisson(1.0)]
    #Anomaly_Error = [poisson(10.0),poisson(1.0),poisson(10.0),poisson(1.0)]

    # Configure the simualtion distribution parameters
    #list_distribution = [norm(5,12),norm(10,20),poisson(10),poisson(100)]

    Gen = Simulation_Generator(list_distribution,Normal_Error,Anomaly_Error,type_error=type_error)

    #Configure the Training_set number
    if incremental == False:
        train_data = Gen.Generate_TrainData(Number_Of_Train)
    else:
        train_data = []
    #print train_data
    return Gen,train_data


def Generate_from_dataset(filename,delimiter,normal_class,column=-1,type_error = "Sudden",incremental = False,percentage = 0.7):
    '''

    :param filename: The simulation data generated from data set
    e.g."./Data/abalone.data"
    :param delimiter: The delimiter of the data set , by default is ","
    :param normal_class: The normal class of one feature
    e.g. 'M'
    :param column: The column of the feature selected for the decision
    e.g. 0
    :param type_error: The type of errors generated in simulation cases
    e.g."Sudden" or "Gradual" or "Outlier"
    :param incremental:If the incremental is true,then no need training data, else, need training data
    :param percentage:if incremental is true, no usage, else, the simulation cases for training data
    :return:
    '''
    #Gen = Dataset_Generator("../Document/abalone.data",",",'M',0 ,type_error="Sudden")
    Gen = Dataset_Generator(filename,delimiter,normal_class,column ,type_error=type_error)
    if incremental ==False:
        # Training percentage
        train_data = Gen.Generate_TrainData(percentage)
    else:
        train_data = []
    return Gen,train_data


def Generate_from_timestamp(filename,delimiter=",",del_timestamp_column=True,timestamp_column=0,percentage=0.7,incremental = False):
    '''

    :param filename:The filepath of the data set in timestamp
    e.g."./Data/abalone.data"
    :param delimiter: The delimiter in the data set,by default ","
    e.g.","
    :param del_timestamp_column: Whether to delete the timestamp column or not, by default, "True"
    e.g.True
    :param timestamp_column: The column of the timestamp in data set
    e.g. 0
    :param percentage: If incremental is false, then percentage is the percentage for the training data set
    :param incremental: whether the stream is trained incrementally
    :return:
    '''
    Gen = Timestamp_Dataset_Generator(filename,delimiter,del_timestamp_column,timestamp_column)
    if incremental ==False:
        # Training percentage
        train_data = Gen.Generate_TrainData(percentage)
    else:
        train_data = []
    return Gen,train_data