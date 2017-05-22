from realTimePred import *
from socket import *
from sklearn.externals import joblib
from math import sqrt
from utils import createSample
import struct
import time
# -----------------MAIN---------------------------------------

HOST = '192.168.4.10' # local machine's IP address
PORT = 9048

address = (HOST, PORT)
client_socket = socket(AF_INET, SOCK_DGRAM) #Set Up the Socket
client_socket.bind((HOST, PORT))
client_socket.settimeout(5) #only wait 5 second for a response, otherwise timeout

start = time.time()

dataBuffer = []

while(1): #Main Loop
    single_var = client_socket.recvfrom(200)
    test = single_var[0]
    #print(test)
    data = struct.unpack('fffffffffffffff',test) #15 floats for sit-stand device and 25 floats for Harness device

    time.sleep(10/1000000) # sleep 10 microseconds
    dataBuffer.append(data)
    if dataBuffer[-1][0] - dataBuffer[0][0] > 0.5:
        print(predict(dataBuffer))
        dataBuffer.clear()
