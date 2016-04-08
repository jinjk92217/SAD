from Stream_Generator.Simulation_Generator import Simulation_Generator
from Stream_Generator.Dataset_Generator import Dataset_Generator
from scipy.stats import poisson,norm
from Stream_Generator.Timestamp_Dataset_Generator import Timestamp_Dataset_Generator

def Generate_from_simulation(Normal_Error,Anomaly_Error,list_distribution,type_error,incremental=False,Number_Of_Train=10000):
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
    #Gen = Dataset_Generator("../Document/abalone.data",",",'M',0 ,type_error="Sudden")
    Gen = Dataset_Generator(filename,delimiter,normal_class,column ,type_error=type_error)
    if incremental ==False:
        # Training percentage
        train_data = Gen.Generate_TrainData(percentage)
    else:
        train_data = []
    return Gen,train_data


def Generate_from_timestamp(filename,delimiter=",",del_timestamp_column=True,timestamp_column=0,percentage=0.7,incremental = False):
    Gen = Timestamp_Dataset_Generator(filename,delimiter,del_timestamp_column,timestamp_column)
    if incremental ==False:
        # Training percentage
        train_data = Gen.Generate_TrainData(percentage)
    else:
        train_data = []
    return Gen,train_data