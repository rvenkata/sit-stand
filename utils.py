import pandas as pd
import numpy as np
from math import sqrt

def calcEnergy(data):
    energy_column = []
    for i in range(0, len(data)):
        row = data.values[i]
        accx = row[2]
        accy = row[3]
        accz = row[4]
        energy = sqrt(accx ** 2 + accy ** 2 + accz ** 2)
        energy_column.append(energy)
    return energy_column


def deleteColumns(data, columns):
    for col in columns:
        del data[col]


def createTarget(data, targetValue):
    target = []
    for i in range(0, len(data)):
        target.append(targetValue)
    return target

def createTargetFromLength(length, targetValue):
    target = []
    for i in range(length):
        target.append(targetValue)
    return target
# split data by specified time intervals returns list of lists that contains indecies that are in the same interval
def createIntervalIndex(data, interval):
    timeStepCounter = 0
    timeStamps = data['timestamp'].values
    lastTimeStep = 0
    lastIndex = 0
    timeIntervalIndices = []
    for i in range(0, len(data)):
        if lastTimeStep == 0:
            lastTimeStep = timeStamps[i]
        currentTimeStamp = timeStamps[i]
        timeStepCounter += (currentTimeStamp - lastTimeStep)
        if timeStepCounter > interval:
            lastTimeStep = 0
            timeStepCounter = 0
            timeIntervalIndices.append(list(range(lastIndex, i + 1)))
            lastIndex = i + 1
        elif i == len(data) - 1:
            timeIntervalIndices.append(list(range(lastIndex, i + 1)))
        else:
            lastTimeStep = currentTimeStamp
    return timeIntervalIndices

def createIntervalDataset(data, interval):
    intervalList = createIntervalIndex(data, interval)
    resultIntervalValues = None
    for interval in intervalList:
        intervalValues = data.values[interval]
        averageIntervalValues = intervalValues.mean(axis=0)
        if resultIntervalValues is None:
            resultIntervalValues = averageIntervalValues
        else:
            resultIntervalValues = np.vstack([resultIntervalValues, averageIntervalValues])
    return pd.DataFrame(data=resultIntervalValues, columns=data.columns)

def createMovingIntervalDataset(data, timeSampleRate):
    resultIntervalValues = None

    for i in range(0, len(data.values)):
        startTimeStamp = data.values[i][0]
        timeIndex = 1

        timeElapsed = 0
        while (timeElapsed < timeSampleRate) and (i + timeIndex) < len(data.values):
            nextTimeStamp = data.values[i + timeIndex][0]
            timeDifference = nextTimeStamp - startTimeStamp
            startTimeStamp = nextTimeStamp
            timeElapsed += timeDifference
            timeIndex += 1

        averageIntervalValues = data.values[range(i, i + timeIndex)].mean(axis=0)

        if resultIntervalValues is None:
            resultIntervalValues = averageIntervalValues
        else:
            resultIntervalValues = np.vstack([resultIntervalValues, averageIntervalValues])

        if i + timeIndex == len(data.values):
            break


    return pd.DataFrame(data=resultIntervalValues, columns=data.columns)

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
