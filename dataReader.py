import pandas as pd
import glob

def makeDataFrameFromFiles(files):
    df = pd.DataFrame()
    list_ = []
    for file_ in files:
        df = pd.read_csv(file_, index_col=None, header=0)
        list_.append(df)
    df = pd.concat(list_)
    return df

def makeDataFrameListsFromFiles(files, colNames):
    df = pd.DataFrame()
    dataFrameList = []
    for file_ in files:
        df = pd.read_csv(file_, index_col=None, header=0)[colNames]
        dataFrameList.append(df)
    return dataFrameList

path = 'data/'
allStandFiles = glob.glob(path + "stand/*.csv")
allSitFiles = glob.glob(path + "sit/*.csv")
allWalkFiles = glob.glob(path + "walk/*.csv")

colNames = ['timestamp', 'Pitch_sensor1', 'accx', 'accy', 'accz']
standData = makeDataFrameFromFiles(allStandFiles)[colNames]
sitData = makeDataFrameFromFiles(allSitFiles)[colNames]
walkData = makeDataFrameFromFiles(allWalkFiles)[colNames]

standDataList = makeDataFrameListsFromFiles(allStandFiles, colNames)
sitDataList = makeDataFrameListsFromFiles(allSitFiles, colNames)
walkDataList = makeDataFrameListsFromFiles(allWalkFiles, colNames)




