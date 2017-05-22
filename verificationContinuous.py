#--------------Test motion example---------------------------------#
# 5 seconds sitting + 5 seconds upright active (sit) + 5 seconds stand
sitToStand = [("sit", 5), ("stand", 5)]

# 5 seconds stand + 5 seconds upright active (stand) + 5 seconds sitting
standToSit = [("stand", 10), ("sit", 10)]

# 3 seconds stand + 24 seconds walk + 3 seconds stand
walk = [("stand", 3), ("walk", 24), ("stand", 3)]

def createPattern(activityArray, testTimeInterval):
    patternArray = []
    for activityEntry in activityArray:
        activity = activityEntry[0]
        durationInSec = activityEntry[1]
        numIteration = float(durationInSec) / testTimeInterval
        for i in range(0, int(numIteration)):
            patternArray.append(activity)
    return patternArray

sitToStandTarget = createPattern(sitToStand, 0.5)
standToSitTarget = createPattern(standToSit, 0.5)
walkTarget = createPattern(walk, 0.5)
print (sitToStandTarget)

def testMotionContinuous(dataset, patterns):
    datasetIndex = 0
    accuracy = 100.0
    for pattern in patterns:
        activity = pattern[0]
        duration = float(pattern[1])
        while duration > 0 and datasetIndex < len(dataset) - 1:
            thisSample = dataset[datasetIndex]
            nextSample = dataset[datasetIndex + 1]
            timeDifference = nextSample[1] - thisSample[1]
            duration -= timeDifference
            datasetIndex += 1
            if activity != thisSample[0]:
                accuracy -= ((1/float(len(dataset))) * 100)

    print("test result: ", accuracy)
  
    
from socket import *
from sklearn.externals import joblib
from math import sqrt
from math import sqrt
from utils import createSample, createMovingIntervalDataset
import struct
import time
from realTimePred import predict, averagePitch

# -----------------MAIN---------------------------------------

HOST = '192.168.4.10' # local machine's IP address
PORT = 9048

address = (HOST, PORT) 
client_socket = socket(AF_INET, SOCK_DGRAM) #Set Up the Socket
client_socket.bind((HOST, PORT)) 
client_socket.settimeout(5) #only wait 5 second for a response, otherwise timeout

start = time.time()

dataBuffer = []
result = []
tEnd = start + 10
print ("current time ", start)
print ("end time", tEnd)
    
while time.time() < tEnd: #Main Loop
    single_var = client_socket.recvfrom(200)
    test = single_var[0]
    #print(test)
    data = struct.unpack('fffffffffffffff',test) #15 floats for sit-stand device and 25 floats for Harness device
    dataBuffer.append(data)
    if dataBuffer[-1][0] - dataBuffer[0][0] > 0.5:
        # sample = createSample(dataBuffer)
        # print(sample)
        # print(clf.predict(sample))
        predictionResult = predict(dataBuffer)
        print (predictionResult)
        result.append((predictionResult, time.time()))
        # dataBuffer.clear()
        dataBuffer.pop(0)
    dataBuffer.append(data)

# for i in range(len(result)):
#     print("expected: ", sitToStandTarget[i])
#     print("result: ", result[i])
#     print("*********************")

# testMotion(result, sitToStandTarget)

for u in result:
    print (u)

testMotionContinuous(result, sitToStand)