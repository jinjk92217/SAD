import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
from matplotlib.widgets import Button
import psutil
plt.close()
#fig = plt.figure()
#ax1 = fig.add_subplot(1,1,1)

fig = plt.figure(figsize=(20,10))
ax1 = fig.add_subplot(1,1,1)
ylim = 20.0
process = 0


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
    first = 0
    info = []
    for eachLine in dataArray:
        if len(eachLine)>1:
            if first == 0:
                first = 1
                info = eachLine.split(' ')
                continue
            x,y,z = eachLine.split(' ')
            xar.append(int(x))
            yar.append(float(y))
            zar.append(int(z))
    ax1.clear()
    ax1.plot(xar,yar)
    ax1.plot(xar,zar,linewidth=5,color='r')
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    textstr=""
    #print len(info)
    if len(info)==5:
        textstr = 'MisDetected_error=%d\nDetected_error=%d\nTotal_error=%d\nRate=%f'%(int(info[1]),int(info[2]),int(info[3]),float(info[4]))
    ax1.text(0.05, 0.95, textstr, transform=ax1.transAxes, fontsize=14,
        verticalalignment='top', bbox=props)
    ax1.set_ylim([0.0, ylim])
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

