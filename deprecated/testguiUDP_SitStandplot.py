# -*- coding: utf-8 -*-

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
from sklearn import svm, metrics
import pickle as cPickle
from math import sqrt

#------------------------------
# UDP specific ----------------
#------------------------------

from socket import *
import time
import struct
import csv

HOST = '192.168.4.10' # local machine's IP address
PORT = 9048

address = (HOST, PORT) 
client_socket = socket(AF_INET, SOCK_DGRAM) #Set Up the Socket
client_socket.bind((HOST, PORT)) 
client_socket.settimeout(10) #only wait 5 second for a response, otherwise timeout
print(AF_INET)
print(client_socket)

f = open('test.csv','wb') 
csv_out = csv.writer(f)
#csv_out.writerow(['timestamp','Qx_sensor1','Qy_sensor1','Qz_sensor1','Qw_sensor1','Heading_sensor1','Pitch_sensor1','Roll_sensor1','Qx_sensor2','Qy_sensor2','Qz_sensor2','Qw_sensor2','Heading_sensor2','Pitch_sensor2','Roll_sensor2','diff_Heading','diff_Pitch','diff_Roll','vel_Heading','vel_Pitch','vel_Roll','acc_Heading','acc_Pitch','acc_Roll','Vbat'])
#csv_out.writerow(['timestamp','Qx_sensor1','Qy_sensor1','Qz_sensor1','Qw_sensor1','Heading_sensor1','Pitch_sensor1','Roll_sensor1','accx','accy','accz','gx','gy','gz','Vbat'])
single_var = client_socket.recvfrom(200)
test = single_var[0]
data = struct.unpack('fffffffffffffff',test) #15 floats for sit-stand device and 25 floats for Harness device
startTime = data[0]    
    
#----------------------------------------
    
# with open('C:\\Anaconda3\\rf_classifier2', 'rb') as f:
    # rf = cPickle.load(f)
    
win = pg.GraphicsWindow()
win.setWindowTitle('pyqtgraph example: Scrolling Plots')

# 3) Plot in chunks, adding one new plot curve for every 100 samples
chunkSize = 100
# Remove chunks after we have 10
maxChunks = 10
startTime = pg.ptime.time()

win.nextRow()
p1 = win.addPlot(colspan=2)
p1.setLabel('bottom', 'Time', 's')
p1.setXRange(-10, 0)
#p1.addLegend()
p1.showGrid(x=10,y=10)

win.nextRow()
p2 = win.addPlot(colspan=2)
p2.setLabel('bottom', 'Time', 's')
p2.setXRange(-10, 0)
#p2.addLegend()
p2.showGrid(x=10,y=10)

win.nextRow()
p3 = win.addPlot(colspan=2)
p3.setLabel('bottom', 'Time', 's')
p3.setXRange(-10, 0)
#p2.addLegend()
p3.showGrid(x=10,y=10)

curves1 = []
curves2 = []
curves3 = []
curves4 = []
curves5 = []
curves6 = []
curves7 = []

data_heading = np.empty((chunkSize+1,2))
data_pitch = np.empty((chunkSize+1,2))
data_roll = np.empty((chunkSize+1,2))

data_accx = np.empty((chunkSize+1,2))
data_accy = np.empty((chunkSize+1,2))
data_accz = np.empty((chunkSize+1,2))
data_classify = np.empty((chunkSize+1,2))

ptr5 = 0
ptr6 = 0

def update3():
    global p1, data_heading, data_pitch, data_roll, ptr5, curves1, curves2, curves3, curves4, curves5, curves6, data_accx, data_accy, data_accz, data_classify
    
    single_var = client_socket.recvfrom(200)
    test = single_var[0]    

    #data= struct.unpack('fffffffffffffffffffffffff',test)
    data = struct.unpack('fffffffffffffff',test) #15 floats for sit-stand device and 25 floats for Harness device
    now = data[0]    
#    csv_out.writerow(data)
    
    
    #print(now-startTime)
    for c in curves1:
        c.setPos(-(now-startTime), 0)
    for c in curves2:
        c.setPos(-(now-startTime), 0)    
    for c in curves3:
        c.setPos(-(now-startTime), 0)    
    for c in curves4:
        c.setPos(-(now-startTime), 0)
    for c in curves5:
        c.setPos(-(now-startTime), 0)    
    for c in curves6:
        c.setPos(-(now-startTime), 0)    
    for c in curves7:
        c.setPos(-(now-startTime), 0)
        
    i = ptr5 % chunkSize
    if i == 0:
        curve1 = p1.plot()
        curve2 = p1.plot()
        curve3 = p1.plot()

        curve4 = p2.plot()
        curve5 = p2.plot()
        curve6 = p2.plot()
        
        curve7 = p3.plot()
        
        curves1.append(curve1)
        curves2.append(curve2)
        curves3.append(curve3)

        curves4.append(curve4)
        curves5.append(curve5)
        curves6.append(curve6)
        
        curves7.append(curve7)
        
        last5 = data_heading[-1]
        data_heading = np.empty((chunkSize+1,2))        
        data_heading[0] = last5
        
        last6 = data_pitch[-1]
        data_pitch = np.empty((chunkSize+1,2))        
        data_pitch[0] = last6  

        last7 = data_roll[-1]
        data_roll = np.empty((chunkSize+1,2))        
        data_roll[0] = last7          
        
        last8 = data_accx[-1]
        data_accx = np.empty((chunkSize+1,2))        
        data_accx[0] = last8
        
        last9 = data_accy[-1]
        data_accy = np.empty((chunkSize+1,2))        
        data_accy[0] = last9  

        last10 = data_accz[-1]
        data_accz = np.empty((chunkSize+1,2))        
        data_accz[0] = last10

        last11 = data_classify[-1]
        data_classify = np.empty((chunkSize+1,2))        
        data_classify[0] = last11        
        
        while len(curves1) > maxChunks:
            c1 = curves1.pop(0)
            p1.removeItem(c1)
            temp=0
        while len(curves2) > maxChunks:
            c2 = curves2.pop(0)
            p1.removeItem(c2)
            temp=0    
    else:
        curve1 = curves1[-1]
        curve2 = curves2[-1]
        curve3 = curves3[-1]
        curve4 = curves4[-1]
        curve5 = curves5[-1]
        curve6 = curves6[-1]
        curve7 = curves7[-1]
        
    if data[6] > -10:
        preds = 1
    else:
        preds = 0  

    energy = sqrt(data[8]*data[8] + data[9]*data[9] + data[10]*data[10])
    preds = rf.predict([data[6], data[8], data[9], data[10], energy])


    if preds == 'sit':
        data_classify[i+1,1] = 0
    elif preds == 'stand':
        data_classify[i+1,1] = 1  
    else:
        data_classify[i+1,1] = 2

        
    data_heading[i+1,0] = now - startTime
    data_heading[i+1,1] = data[5]
    
    data_pitch[i+1,0] = now - startTime
    data_pitch[i+1,1] = data[6]
    
    data_roll[i+1,0] = now - startTime
    data_roll[i+1,1] = data[7]

    data_accx[i+1,0] = now - startTime
    data_accx[i+1,1] = data[8]
    
    data_accy[i+1,0] = now - startTime
    data_accy[i+1,1] = data[9]
    
    data_accz[i+1,0] = now - startTime
    data_accz[i+1,1] = data[10]
    
    data_classify[i+1,0] = now - startTime
    data_classify[i+1,1] = preds
    
    energy = (data[8]*data[8] + data[9]*data[9] + data[10]*data[10])
    
    curve1.setData(x=data_heading[:i+2, 0], y=data_heading[:i+2, 1],pen='r', name ='Heading')
    curve2.setData(x=data_pitch[:i+2, 0], y=data_pitch[:i+2, 1],pen='g', name ='Pitch') 
    curve3.setData(x=data_roll[:i+2, 0], y=data_roll[:i+2, 1],pen='b', name ='Roll') 
    curve4.setData(x=data_accx[:i+2, 0], y=data_accx[:i+2, 1],pen='r', name ='Accx')
    curve5.setData(x=data_accy[:i+2, 0], y=data_accy[:i+2, 1],pen='g', name ='Accy') 
    curve6.setData(x=data_accz[:i+2, 0], y=data_accz[:i+2, 1],pen='b', name ='Accz') 
    curve7.setData(x=data_classify[:i+2, 0], y=data_classify[:i+2, 1],pen='b', name ='Prediction') 
    
    
    # if energy >0.3:
        # preds = 2
    # else:
        # if pitch > -10:
            # preds = 1
        # else:
            # preds = 0
        
        
    #preds = rf.predict([data[6], energy])
    print(preds)

    ptr5 += 1

# update all plots
def update():
    update3()
    
timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(20)

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
