from socket import *
from sklearn.externals import joblib
from math import sqrt
from math import sqrt
from utils import createSample
import struct
import time


def createSample(dataset):
    datasetSize = float(len(dataset))
    sample = [0, 0, 0, 0, 0]
    for data in dataset:
        energy = sqrt(data[8]*data[8] + data[9]*data[9] + data[10]*data[10])
        sample[0] += data[6]
        sample[1] += data[8]
        sample[2] += data[9]
        sample[3] += data[10]
        sample[4] += energy

    for i in range(0, len(sample)):
        sample[i] = sample[i] / datasetSize

    return sample

# -----------------MAIN---------------------------------------
clf = joblib.load('model/rf_classifier.pkl') 

HOST = '192.168.4.10' # local machine's IP address
PORT = 9048

address = (HOST, PORT) 
client_socket = socket(AF_INET, SOCK_DGRAM) #Set Up the Socket
client_socket.bind((HOST, PORT)) 
client_socket.settimeout(5) #only wait 5 second for a response, otherwise timeout

start = start = time.time()

dataBuffer = []

while(1): #Main Loop
    single_var = client_socket.recvfrom(200)
    test = single_var[0]
    #print(test)
    data = struct.unpack('fffffffffffffff',test) #15 floats for sit-stand device and 25 floats for Harness device

    time.sleep(10/1000000) # sleep 10 microseconds
    dataBuffer.append(data)
    if dataBuffer[-1][0] - dataBuffer[0][0] > 1:
        sample = createSample(dataBuffer)
        print(sample)
        print(clf.predict(sample))
        dataBuffer.pop(0)