from Stream_Generator.Simulation_Generator import Simulation_Generator
from Stream_Generator.Dataset_Generator import Dataset_Generator
from scipy.stats import poisson,norm
from Point_AnomalyDetector.PyiscAnomalyScorer import PyiscAnomalyScorer
from Point_AnomalyDetector.LOFAnomalyScorer import LOFAnomalyScorer
from Stream_AnomalyDetector.Stream_Detector import Stream_Detector
import time
import numpy as np
import random

Error_rate = 0.1   #error rate happened
Mean_number = 200  # the mean number of errors happened when a error happens
Train_incremental = False      # whether train the data incrementally


Total_error = 0      # count the number of error happened in the program
Detected_error = 0   # count the number of detected errors from detectors
MisDetect_error = 0  # count the number of misdetected errors from detectors
Total_number = 0     # Total number of cases
Plot_Window_Size = 2000    # the plot window size
Series_array = [0] * Plot_Window_Size
Score_array = [0] * Plot_Window_Size
Detected_array = [0] * Plot_Window_Size



Shift_times = 1000   # the total time of changes between normal and anomaly cases
stream_array = []



data_source_type = "simulation"   # Choose the data source, either simulation or data_set
Point_detector_type = "pyisc"     # Choose the point anomaly detectors, either pyisc or lof
Stream_detector_type = "CUSUM"      # Choose the stream anomaly detectors, either DDM or CUSUM
error_type = "Sudden"            # Choose the type of errors, could be Sudden, Outlier and Gradual
random.seed(100)




if data_source_type == "simulation":
    #simulation data setup

    #Configure the Normal_error or Anomaly_error distribution
    Normal_Error = poisson(1.0)
    Anomaly_Error = poisson(10.0)

    # Configure the simualtion distribution parameters
    list_distribution = [norm(5,12),norm(10,20),poisson(10),poisson(100)]

    Gen = Simulation_Generator(list_distribution,Normal_Error,Anomaly_Error)

    #Configure the Training_set number
    train_data = Gen.Generate_TrainData(10000)
    #print train_data
elif data_source_type == "data_set":
    #data set setup

    #Parameters:file_path, delimiter, normal_class, column of normal_class
    Gen = Dataset_Generator("../Document/abalone.data",",",'M',0 )

    # Training percentage
    train_data = Gen.Generate_TrainData(0.7)



if Point_detector_type == "pyisc":
    Point_Detector = PyiscAnomalyScorer()
elif Point_detector_type == "lof":
    Point_Detector = LOFAnomalyScorer()


if Stream_detector_type  == "DDM":
    Stream_Detector = Stream_Detector("DDM.so",[3.0]) # for pyisc
    #Stream_Detector = Stream_Detector("DDM.so",[1.1]) # for lof
elif Stream_detector_type == "CUSUM":
    Stream_Detector = Stream_Detector("CUSUM.so",[1.0,11.0])
elif Stream_detector_type  == "DDM_window":
    Stream_Detector = Stream_Detector("CUSUM_window.so",[2.0,3.0])

anomaly_detector = Point_Detector.Train_PointDetector(train_data)





def write_to_file(Info):
    datafile_path = "datafile.txt"
    datafile_id = open(datafile_path, 'w+')
    #here you open the ascii file

    #xarray = np.array([0,1,2,3,4,5])
    #yarray = np.array([0,10,20,30,40,50])
    #here is your data, in two numpy arrays
    infostr="Information"
    for x in Info:
        infostr = infostr +" " +str(x)
    datafile_id.write(infostr+"\n")
    data = np.array([Series_array, Score_array,Detected_array])
    data = data.T
    #here you transpose your data, so to have it in two columns

    np.savetxt(datafile_id, data, fmt=['%d','%f','%d'])
    #here the ascii file is populated.

    datafile_id.close()
    #close the file



if __name__ == '__main__':
    if_error = 0
    total_number = 0
    start_time = time.time()
    current_time = 0
    #while 1:
    for loops in xrange(Shift_times):
        if random.uniform(0.0, 1.0)>Error_rate:
            if_error = False
        else:
            if_error = True
        number = poisson(Mean_number).rvs(1)[0]
        Detect_flag = 0
        flag = 0
        anomaly_flag = 0
        if if_error == True:
            stream_array=np.matrix(Gen.Generate_Stream(error_type,number))
        else:
            stream_array =np.matrix(Gen.Generate_Stream("Normal",number))
        if len(stream_array)<number:
            number = len(stream_array)
        for i in xrange(number):
            Total_number = Total_number + 1
            if (if_error ==True and flag ==0):
                print "start error!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!   size    ",number
                flag = 1
                Total_error = Total_error + 1
            total_number = total_number + 1
            tmp =stream_array[i,:]
            score = anomaly_detector.anomaly_score(tmp)[0]
            if Train_incremental == True:
                anomaly_detector.fit_incrementally(tmp)
            anomaly_flag = 0
            if Stream_Detector.classifier(score)==1:
                anomaly_flag = 10
                print "drift",if_error,score
                if if_error ==True and Detect_flag == 0:
                    Detected_error = Detected_error + 1
                    Detect_flag = 1
                elif if_error != True:
                    MisDetect_error = MisDetect_error + 1
                current_time = time.time() - start_time
                print "Current accuracy",MisDetect_error,Detected_error,Total_error,Total_number,current_time,Total_number/current_time
            Series_array[Total_number%Plot_Window_Size] = Total_number
            Score_array[Total_number%Plot_Window_Size] = score
            Detected_array[Total_number%Plot_Window_Size] = anomaly_flag
            if Total_number%Plot_Window_Size == Plot_Window_Size-1:
                try:
                    current_time = time.time() - start_time
                    write_to_file([MisDetect_error,Detected_error,Total_error,Total_number/current_time])
                except Exception as e:
                    print e


