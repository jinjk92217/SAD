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
Plot_ylim = 10

Shift_times = 1000   # the total time of changes between normal and anomaly cases
stream_array = []

random.seed(10)
Gen,train_data = Config_Generator.Generate_from_timestamp(
        filename = "./Data/rogue_agent_key_updown.csv",
        # filename = "./Data/art_daily_small_noise.csv",
        # filename = "./Data/Twitter_volume_GOOG.csv",
        delimiter=",",
        del_timestamp_column=True,
        timestamp_column=0,
        percentage=0.7,
        incremental = Train_incremental
)

# print train_data
anomaly_detector = Config_PointDetector.pyisc_PointDetector(
    train_data= train_data,
    #models = [],
    #models=[pyisc.P_Gaussian(1),pyisc.P_Gaussian(2),pyisc.P_Poisson(3,0),pyisc.P_Poisson(4,0)],
    models=[pyisc.P_Gaussian(0)],
    incremental= Train_incremental,
    # test_distribution=['norm']
)


# anomaly_detector = Config_PointDetector.lof_PointDetector(
#     train_data=train_data,
#     n_neighbors = 10,
#     algorithm = 'auto'
# )



#
# Stream_Detector = Config_StreamDetector.DDM_StreamDetector(
#     #filename = "./Stream_AnomalyDetector/C++/DDM.so",
#     threshold = 1.5
# )

Stream_Detector = Config_StreamDetector.CUSUM_StreamDetector(
    #filename = "./Stream_AnomalyDetector/C++/CUSUM.so",
    drift = 1.0,
    threshold = 12.0
    # drift = 0.2,
    # threshold = 3.0
    # drift = 0.1,
    # threshold = 0.6
)



def write_to_file(Info,size=Plot_Window_Size):
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




#if __name__ != '__main__' or 1==1:
#if __name__ == '__main__':
def test_process():
    global Error_rate,Mean_number,Train_incremental,Total_error,Detected_error,MisDetect_error,Total_number,Plot_Window_Size,Series_array,Score_array,Detected_array
    global Shift_times,stream_array,Gen,train_data,anomaly_detector,Stream_Detector
    if_error = 0
    start_time = time.time()
    current_time = 0
    while 1:
    #for loops in xrange(Shift_times):
        Total_number = Total_number + 1
        tmp =Gen.Generate_Stream()
        if tmp == []:
            break
        score = anomaly_detector.anomaly_score(tmp)[0]
        # print "score",tmp
        if Train_incremental == True:
            anomaly_detector.fit_incrementally(tmp)
        anomaly_flag = 0
        if Stream_Detector.check(score)==1:
            anomaly_flag = Plot_ylim/2
            print "drift",if_error,score
            Detected_error = Detected_error + 1
            #current_time = time.time() - start_time
        Series_array[Total_number%Plot_Window_Size] = Total_number
        Score_array[Total_number%Plot_Window_Size] = score
        Detected_array[Total_number%Plot_Window_Size] = anomaly_flag
        if Total_number%Plot_Window_Size == Plot_Window_Size-1:
            try:
                current_time = time.time() - start_time
                write_to_file([MisDetect_error,Detected_error,Total_error,Total_number/current_time])
            except Exception as e:
                print e
    try:
        current_time = time.time() - start_time
        write_to_file([MisDetect_error,Detected_error,Total_error,Total_number/current_time],size=Total_number%Plot_Window_Size)
    except Exception as e:
        print e


def runplot():
    import Plot_process
    Plot_process.set_ylim(Plot_ylim)
    Plot_process.plot_process()
    #Plot_process.pl()

if __name__ == '__main__':
    process1 = multiprocessing.Process(target=test_process, args=[])
    process2 = multiprocessing.Process(target=runplot, args=[])
    process1.start()
    time.sleep(1)

    process2.start()
    '''
    time.sleep(5)
    p = psutil.Process(process1.pid)
    p.suspend()
    time.sleep(5)
    p.resume()
    '''