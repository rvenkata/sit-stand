#--------------Test motion example---------------------------------#
sitToStand = [("sit", 10), ("stand", 10), ("sit", 10)]

standToSit = [("stand", 10), ("sit", 10), ("stand", 10)]

walkAndStop = [("stand", 10), ("walk", 30), ("stand", 10), ("walk", 30), ("stand", 10), ("sit", 10)]

walkSlow = [("sit", 10), ("stand", 10), ("walk", 20), ("stand", 10), ("sit", 10)] 

walkNormal = [("sit", 10), ("stand", 10), ("walk", 20), ("stand", 10), ("sit", 10)]

walkFast = [("sit", 10), ("stand", 10), ("walk", 20), ("stand", 10), ("sit", 10)]

#-----------------------------------------------------------------#

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
walkTarget = createPattern(walkFast, 0.5)
print (sitToStandTarget)

def testMotion(dataset, pattern, interval, threshold):
    target = createPattern(pattern, interval)
    sample = predictFullDatasetWithInterval(dataset, interval, threshold)

    target = target[0: min(len(sample), len(target))]
    sample = sample[0: min(len(sample), len(target))]

    accuracy = 100.0

    for i in range(len(sample)):
        targetVal = target[i]
        sampleVal = sample[i]
        if targetVal != sampleVal:
            accuracy -= ((1 / float(len(sample))) * 100.0)

    print("test result: ", accuracy)
    return accuracy

def testHyperParam(datasets, patterns):
    maxHyperParams = []

    for i in range(len(datasets)):
        interval = 0.30
        epsilon = 0.01
        dataset = datasets[i]
        pattern = patterns[i]

        maxAccuracy = 0
        bestHyperParams = {"interval" : 0, "threshold" : 0, "accuracy" : 0}
        while interval <= 1.50:
            threshold = 0.20
            while threshold <= 0.50:
                testAccuracy = testMotion(dataset, pattern, interval, threshold)
                if testAccuracy > maxAccuracy:
                    maxAccuracy = testAccuracy
                    bestHyperParams["interval"] = interval
                    bestHyperParams["threshold"] = threshold
                    bestHyperParams["accuracy"] = maxAccuracy
                threshold += epsilon
            interval += epsilon
        maxHyperParams.append(bestHyperParams)

    return maxHyperParams

from socket import *
from sklearn.externals import joblib
from math import sqrt
from math import sqrt
from utils import createSample, createIntervalDataset
import struct
import time
from realTimePred import predict, averagePitch, predictFullDatasetWithInterval
from dataReader import makeDataFrameFromFiles, colNames
import glob

# ---- READ IN TEST DATA ------------------------------------------------------------------
path = path = 'data/'
sitToStandData = makeDataFrameFromFiles(glob.glob(path + "/verification/sitToStand.csv"))
print (sitToStandData)
# -----------------------------------------------------------------------------------------


# -----------------MAIN---------------------------------------

HOST = '192.168.4.10' # local machine's IP address
PORT = 9048
RMS_THRESHOLD = 0.3

address = (HOST, PORT) 
client_socket = socket(AF_INET, SOCK_DGRAM) #Set Up the Socket
client_socket.bind((HOST, PORT)) 
client_socket.settimeout(5) #only wait 5 second for a response, otherwise timeout

start = time.time()

dataBuffer = []
result = []
tEnd = start + 20
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
        predictionResult = predict(dataBuffer, RMS_THRESHOLD)
        print (predictionResult)
        result.append(predictionResult)
        dataBuffer.clear()
        # dataBuffer.pop(0)
    dataBuffer.append(data)

for i in range(len(result)):
    print("expected: ", sitToStandTarget[i])
    print("result: ", result[i])
    print("*********************")

testMotion(result, sitToStandTarget)