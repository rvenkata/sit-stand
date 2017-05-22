from math import sqrt
from utils import createSample, createMovingIntervalDataset


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

def averagePitch(dataset):
    avgPitch = 0
    pitchIndex = 1
    notTruncated = len(dataset[0]) == 15
    if notTruncated:
        pitchIndex += 5
    for data in dataset:
        avgPitch += data[pitchIndex]
    return avgPitch / float(len(dataset))

def predict (dataBuffer, threshold):
    newDataBuffer = []
    xMean = 0
    yMean = 0
    zMean = 0
    sample = dataBuffer[0]
    notTruncated = len(sample) == 15
    for i in range(0, len(dataBuffer) - 1):
        newData = [0, 0, 0]
        thisSample = dataBuffer[i]
        nextSample = dataBuffer[i + 1]

        accxIndex = 2
        accyIndex = 3
        acczIndex = 4

        if notTruncated:
            accxIndex += 6
            accyIndex += 6
            acczIndex += 6

        newData[0] = thisSample[accxIndex] - nextSample[accxIndex]
        newData[1] = thisSample[accyIndex] - nextSample[accyIndex]
        newData[2] = thisSample[acczIndex] - nextSample[acczIndex]

        newDataBuffer.append(newData)
        xMean += newData[0]
        yMean += newData[1]
        zMean += newData[2]

    xMean = xMean / len(newDataBuffer)
    yMean = yMean / len(newDataBuffer)
    zMean = zMean / len(newDataBuffer)

    RMS = []
    for data in newDataBuffer:
        rmsVal = sqrt(((data[0] - xMean) ** 2) + ((data[1] - yMean) ** 2) + ((data[2] - zMean) ** 2))
        RMS.append(rmsVal)

    # meanRMS = sum(RMS) / float(len(RMS))

    for rmsVal in RMS:
        if rmsVal > threshold:
            return "walk"

    else:
        avgPitch = averagePitch(dataBuffer)
        # check pitch
        if avgPitch < -10.0:
            return "sit"
        else:
            return "stand"

def predictFullDatasetWithInterval(dataset, interval, threshold):
    dataBuffer = []
    result = []
    dataset = dataset[1: len(dataset)]
    for i in range(len(dataset)):
        datum = dataset.values[i]
        dataBuffer.append(datum)
        if type(dataBuffer[-1][0]) != str and type(dataBuffer[0][0]) != str and dataBuffer[-1][0] - dataBuffer[0][0] > interval:
            result.append(predict(dataBuffer, threshold))
            dataBuffer.clear()
    return result