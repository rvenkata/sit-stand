from utils import *
from dataReader import *
from sklearn import metrics
from realTimePred import predictFullDatasetWithInterval

# new method to predict
def verify(dataList, targetValue, interval=0.92, threshold=0.2):
    yPred = []
    for x in dataList:
        yPred += predictFullDatasetWithInterval(x, interval, threshold)
    y = createTargetFromLength(len(yPred), targetValue)
    print(metrics.confusion_matrix(y, yPred, labels=['sit', 'stand', 'walk']))
    print(metrics.classification_report(y, yPred, labels=['sit', 'stand', 'walk']))


def accuracyTest(interval, threshold):
    yPred = []
    y = []
    sitYPred = []
    standYPred = []
    walkYPred = []

    for x in sitDataList:
        sitYPred += predictFullDatasetWithInterval(x, interval, threshold)

    for x in standDataList:
        standYPred += predictFullDatasetWithInterval(x, interval, threshold)

    for x in walkDataList:
        walkYPred += predictFullDatasetWithInterval(x, interval, threshold)

    yPred += sitYPred
    yPred += standYPred
    yPred += walkYPred
    y += createTargetFromLength(len(sitYPred), 'sit')
    y += createTargetFromLength(len(standYPred), 'stand')
    y += createTargetFromLength(len(walkYPred), 'walk')

    print(metrics.confusion_matrix(y, yPred, labels=['sit', 'stand', 'walk']))
    print(metrics.classification_report(y, yPred, labels=['sit', 'stand', 'walk']))
    print(metrics.accuracy_score(y, yPred))
    return metrics.accuracy_score(y, yPred)


def testHyperParam():
    maxHyperParams = []

    interval = 0.30
    epsilon = 0.01

    maxAccuracy = 0
    lastAccuracy = 0
    bestHyperParams = {"interval" : 0, "threshold" : 0, "accuracy" : 0}
    while interval <= 1.50:
        threshold = 0.20
        while threshold <= 0.35:
            print ("****interval:, ", interval, "threshold: ", threshold, "****")
            testAccuracy = accuracyTest(interval, threshold)
            if lastAccuracy > testAccuracy:
                break
            if testAccuracy > maxAccuracy:
                maxAccuracy = testAccuracy
                bestHyperParams["interval"] = interval
                bestHyperParams["threshold"] = threshold
                bestHyperParams["accuracy"] = maxAccuracy
                lastAccuracy = testAccuracy
            threshold += epsilon
        interval += epsilon
    maxHyperParams.append(bestHyperParams)

    return maxHyperParams