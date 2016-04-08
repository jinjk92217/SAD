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
Plot_ylim =20

Shift_times = 1000   # the total time of changes between normal and anomaly cases
stream_array = []
np.random.seed(10)
random.seed(10)

Gen,train_data=Config_Generator.Generate_from_simulation(
    Normal_Error = [0,poisson(1.0),poisson(1.0),poisson(1.0),poisson(1.0)],
    Anomaly_Error = [0,poisson(1.0),poisson(1.0),poisson(10.0),poisson(1.0)],
    list_distribution = [1,norm(5,12),norm(10,20),poisson(10),poisson(100)],
    type_error = "Sudden",
    incremental=Train_incremental,
    Number_Of_Train = 10000
)

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


# Stream_Detector = Config_StreamDetector.DDM_StreamDetector(
#     #filename = "./Stream_AnomalyDetector/C++/DDM.so",
#     threshold = 3.0
# )

Stream_Detector = Config_StreamDetector.CUSUM_StreamDetector(
    #filename = "./Stream_AnomalyDetector/C++/CUSUM.so",
    drift = 1.0,
    threshold = 12.0
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
    #total_number = 0
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
                elif if_error != True:
                    MisDetect_error = MisDetect_error + 1
                #current_time = time.time() - start_time
                print "Current accuracy",MisDetect_error,Detected_error,Total_error,Total_number
                #print "Current accuracy",MisDetect_error,Detected_error,Total_error,Total_number,current_time,Total_number/current_time
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

def runplot(pid):
    import Plot_process
    Plot_process.set_ylim(Plot_ylim)
    Plot_process.setpid(pid)
    Plot_process.plot_process()
    #Plot_process.pl()

if __name__ == '__main__':
    process1 = multiprocessing.Process(target=test_process, args=[])
    process1.start()
    time.sleep(0.5)
    process2 = multiprocessing.Process(target=runplot, args=[process1.pid])
    process2.start()
    '''
    time.sleep(5)
    p = psutil.Process(process1.pid)
    p.suspend()
    time.sleep(5)
    p.resume()
    '''