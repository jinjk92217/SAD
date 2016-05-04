"""
:copyright: (c) 2016 Jiakun Jin
email: jiakun@kth.se
:license: LGPL?
"""
import time
import numpy as np
import random
import pyisc
from scipy.stats import poisson,norm
import Config_Generator
import Config_PointDetector
import Config_StreamDetector
import multiprocessing
import psutil

__author__ = 'jiakun'

import Config_seed
Config_seed.Myseed = 119

Plot_ylim =20              #ylim of the plot
Train_incremental = False      # whether train the data incrementally for point anomaly detector
Stream_Train_incremental = True  #Whether train the data incrementally for stream anomaly detector, only when Point anomaly detector being true works
Stream_Train_number = 10000  # if training stream is true, then the number is the training stream number
Error_rate = 0.1            #error rate happened
Mean_number = 200           #the mean number of cases happened during one shift
Shift_times = 1000          #the total time of changes between normal and anomaly cases


Plot_Window_Size = 2000    # the plot window size
Series_array = [0] * Plot_Window_Size
Score_array = [0] * Plot_Window_Size
Detected_array = [0] * Plot_Window_Size



Gen,train_data=Config_Generator.Generate_from_simulation(
    Normal_Error = [0,poisson(1.0),poisson(1.0),poisson(1.0),poisson(1.0)],
    Anomaly_Error = [0,poisson(1.0),poisson(1.0),poisson(10.0),poisson(1.0)],
    list_distribution = [1,norm(5,12),norm(10,20),poisson(10),poisson(100)],
    type_error = "Sudden",
    incremental=Train_incremental,
    Number_Of_Train = 10000
)
#
# Gen,train_data = Config_Generator.Generate_from_dataset(
#     filename = "./Data/abalone.data",
#     delimiter = ",",
#     normal_class = 'M',
#     column = 0,
#     type_error = "Sudden",
#     incremental= Train_incremental,
#     percentage = 0.7
# )

anomaly_detector = Config_PointDetector.pyisc_PointDetector(
    train_data= train_data,
    #models = [],
    models=[pyisc.P_Gaussian(1),pyisc.P_Gaussian(2),pyisc.P_Poisson(3,0),pyisc.P_Poisson(4,0)],
    # models=[pyisc.P_Gaussian([0,1,2,3])],
    incremental= Train_incremental,
    # test_distribution=['norm']
)

# anomaly_detector = Config_PointDetector.lof_PointDetector(
#     train_data=train_data,
#     n_neighbors = 10,
#     algorithm = 'auto'
# )


# anomaly_detector = Config_PointDetector.SVM_PointDetector(
#     train_data=train_data,
#     nu = 0.1,
#     kernel = "rbf",#"poly", "rbf", "sigmoid"
#     gamma = 0.1,
#     coefficient = 0.1#1.0
# )
# #
# Stream_Detector = Config_StreamDetector.DDM_StreamDetector(
#     #filename = "./Stream_AnomalyDetector/C++/DDM.so",
#     threshold = 4.00,#15.0
#     alpha= 2.0,
#     beta= 3.0
# )
#
# Stream_Detector = Config_StreamDetector.CUSUM_StreamDetector(
#     #filename = "./Stream_AnomalyDetector/C++/CUSUM.so",
#     drift = 1.0,
#     threshold = 12.0
# )


Stream_Detector = Config_StreamDetector.FCWM_StreamDetector(
    #filename = "./Stream_AnomalyDetector/C++/CUSUM.so",
    number_bin = 200,
    ref_size=10000,
    rec_size=200,
    maxn=20.0,
    update_able=False,
    Lambda=2.0
)

# Stream_Detector = Config_StreamDetector.PRAAG_StreamDetector(
#     r = 250,
#     l = 1000,
#     e = 0.0001,
#     a = 30.0,
#     k = 0.01
# )


def write_to_file(Info,size=Plot_Window_Size):
    '''
    Write the Info to datafile.data inorder to show the plot in the other process

    :param Info:Points need to be plotted, size: the number of points to be plotted in one time
    :return:
    '''
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
    data = np.array([Series_array[:size], Score_array[:size],Detected_array[:size]])
    data = data.T
    #here you transpose your data, so to have it in two columns

    np.savetxt(datafile_id, data, fmt=['%d','%f','%d'])
    #here the ascii file is populated.

    datafile_id.close()
    #close the file



def test_process(Error_rate = Error_rate,Mean_number = Mean_number,Shift_times = Shift_times, Train_incremental =Train_incremental):
    '''
    This is for data from the simluation and data_set process
    The process will last for Shift_times
    During one shift time, there will be around Mean_number of cases
    There will be around Error_rate percentage error occurs
    :param Error_rate:error rate happened, Mean_number: the mean number of cases happened during one shift,
           Shift_times:the total time of changes between normal and anomaly cases, Train_incremental: Whether Training the case incrementally
    :return:
    '''
    np.random.seed(Config_seed.Myseed)
    random.seed(Config_seed.Myseed)
    Total_error = 0      # count the number of error happened in the program
    Detected_error = 0   # count the number of detected errors from detectors
    MisDetect_error = 0  # count the number of misdetected errors from detectors
    radio_Detect_error = 0.0
    radio_MisDetect_error = 0.0
    Total_number = 0     # Total number of cases
    Delay_number = 0
    Delay_time = 0
    Delay_average_number = 0
    global Plot_Window_Size,Series_array,Score_array,Detected_array
    global Gen,train_data,anomaly_detector,Stream_Detector
    stream_array = []
    if_error = 0
    #total_number = 0
    start_time = time.time()
    current_time = 0
    #while 1:
    for loops in xrange(Shift_times):
        if Stream_Train_incremental==True and Train_incremental == False and loops == 0:
            number = Stream_Train_number
            if_error = False
            Shift_times = Shift_times + 1
        else:
            if random.uniform(0.0, 1.0)>Error_rate:
                if_error = False
            else:
                if_error = True
            number = poisson(Mean_number).rvs(1)[0]
        Detect_flag = 0
        flag = 0
        anomaly_flag = 0
        if if_error == True:
            stream_array=np.matrix(Gen.Generate_Stream("Anomaly",number))
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
            #total_number = total_number + 1
            tmp =stream_array[i,:]
            score = anomaly_detector.anomaly_score(tmp)[0]
            if Train_incremental == True:
                anomaly_detector.fit_incrementally(tmp)
            anomaly_flag = 0
            if Stream_Detector.check(score)==1:
                anomaly_flag = Plot_ylim/2
                print "drift",if_error,score
                if if_error ==True and Detect_flag == 0:
                    Detected_error = Detected_error + 1
                    Detect_flag = 1
                    Delay_number = Delay_number + i
                    Delay_time = Delay_time + 1
                    Delay_average_number = 1.0 * Delay_number / Delay_time
                    if Total_error > 0:
                        radio_Detect_error = 1.0 * Detected_error / Total_error
                elif if_error != True:
                    MisDetect_error = MisDetect_error + 1
                    if Total_error > 0:
                        radio_MisDetect_error = 1.0 * MisDetect_error / Total_error
                #current_time = time.time() - start_time
                print "Current accuracy",MisDetect_error,Detected_error,Total_error,Total_number
                #print "Current accuracy",MisDetect_error,Detected_error,Total_error,Total_number,current_time,Total_number/current_time
            Series_array[Total_number%Plot_Window_Size] = Total_number
            Score_array[Total_number%Plot_Window_Size] = score
            Detected_array[Total_number%Plot_Window_Size] = anomaly_flag
            if Total_number%Plot_Window_Size == Plot_Window_Size-1:
                try:
                    current_time = time.time() - start_time
                    write_to_file([MisDetect_error,Detected_error,Total_error,Total_number/current_time,Delay_average_number,radio_MisDetect_error,radio_Detect_error])
                except Exception as e:
                    print e
    try:
        current_time = time.time() - start_time
        write_to_file([MisDetect_error,Detected_error,Total_error,Total_number/current_time,Delay_average_number,radio_MisDetect_error,radio_Detect_error],size=Total_number%Plot_Window_Size)
    except Exception as e:
        print e

def runplot(pid,Plot_ylim = Plot_ylim):
    '''
    This is for call the plot processing
    :param Error_rate: pid the main_process pid in order to stop and start the main_process
           Plot_ylim: the ylim of the plot
    :return:
    '''
    import Plot_process
    Plot_process.set_ylim(Plot_ylim)
    Plot_process.setpid(pid)
    Plot_process.plot_process()
    #Plot_process.pl()

if __name__ == '__main__':
    process1 = multiprocessing.Process(target=test_process, args=[])
    process1.start()
    time.sleep(0.5)
    process2 = multiprocessing.Process(target=runplot,args=[process1.pid])
    process2.start()
    '''
    time.sleep(5)
    p = psutil.Process(process1.pid)
    p.suspend()
    time.sleep(5)
    p.resume()
    '''