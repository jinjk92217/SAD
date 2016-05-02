import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
from matplotlib.widgets import Button
import psutil
plt.close()
#fig = plt.figure()
#ax1 = fig.add_subplot(1,1,1)

#tag: return A
TMP="PRAAG"

fig = plt.figure(figsize=(30,10))
if TMP == "PRAAG":
    ax1 = fig.add_subplot(2,1,1,ylim=[0.0,20.0])
    ax1_1 = fig.add_subplot(2,1,2,ylim=[0.0,30.0])
else:
    ax1 = fig.add_subplot(1,1,1,ylim=[0.0,20.0])

ylim = 30.0
process = 0
## #tag: return A


def setpid(pid):
    global process
    process = psutil.Process(pid)
    print "pid ",pid


def stop(event):
    process.suspend()
def start(event):
    process.resume()

axstart = plt.axes([0.01, 0.90, 0.06, 0.075])
bstart = Button(axstart, 'Start')
bstart.on_clicked(start)
axpause = plt.axes([0.01, 0.80, 0.06, 0.075])
bpause = Button(axpause, 'Pause')
bpause.on_clicked(stop)


def animate(i):
    #print "hear"
    pullData = open("datafile.txt","r").read()
    dataArray = pullData.split('\n')
    xar = []
    yar = []
    zar = []

    #tag: return A
    aar = []
    first = 0
    info = []
    for eachLine in dataArray:
        if len(eachLine)>1:
            if first == 0:
                first = 1
                info = eachLine.split(' ')
                continue
            #tag: return A
            # x,y,z = eachLine.split(' ')
            x,y,z,a = eachLine.split(' ')
            xar.append(int(x))
            yar.append(float(y))
            zar.append(int(z))
            #tag: return A
            aar.append(float(a))

    ax1.clear()
    ax1.plot(xar,yar)
    ax1.plot(xar,zar,linewidth=5,color='r')

    #tag: return A
    if TMP == "PRAAG":
        ax1_1.clear()
        # ax1_1.plot(xar,yar)
        ax1_1.plot(xar,aar,linewidth=2,color='y')
        ax1_1.plot(xar,zar,linewidth=5,color='r')


    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    textstr=""
    #print len(info)
    if len(info)==8:
        textstr = 'FalseDetected_error=%d\nDetected_error=%d\nTotal_error=%d\nRate=%f\nDelay=%f\nFalsedetected_percentage=%f\nDetected_percentage=%f'%(int(info[1]),int(info[2]),int(info[3]),float(info[4]),float(info[5]),float(info[6]),float(info[7]))
    ax1.text(0.05, 0.95, textstr, transform=ax1.transAxes, fontsize=14,
        verticalalignment='top', bbox=props)
    ax1.set_ylim([0.0, ylim])
    if TMP == "PRAAG":
        ax1_1.text(0.05, 0.95, textstr, transform=ax1_1.transAxes, fontsize=14,
            verticalalignment='top', bbox=props)
    #time.sleep(10)
#ani = animation.FuncAnimation(fig, animate, interval=1000)
#plt.show()

def set_ylim(y):
    global ylim
    ylim = y
def plot_process():
#if __name__ != '__main__' or 1==1:
#if __name__ == '__main__':
    ani = animation.FuncAnimation(fig, animate, interval=500)
    plt.show()
if __name__ == '__main__':
    plot_process()

