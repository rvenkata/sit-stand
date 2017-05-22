from utils import *
import matplotlib.pyplot as plt

# reading data from csv
colnames = ['timestamp', 'Pitch_sensor1', 'accx', 'accy', 'accz']
sitData = pd.read_csv('data/test_sit.csv', sep=',', usecols=colnames)
standData = pd.read_csv('data/test_stand.csv', sep=',', usecols=colnames)
walkData = pd.read_csv('data/test_walk.csv', sep=',', usecols=colnames)
sitDataKenneth = pd.read_csv('data/test_sit_Kennethdata.csv', sep=',', usecols=colnames)
standDataKenneth = pd.read_csv('data/test_stand_Kennethdata.csv', sep=',', usecols=colnames)
walkDataKenneth = pd.read_csv('data/test_walk_Kennethdata.csv', sep=',', usecols=colnames)

sitDataKenneth2 = pd.read_csv('data/test_sit_Kennethdata2.csv', sep=',', usecols=colnames)
standDataKenneth2 = pd.read_csv('data/test_stand_Kennethdata2.csv', sep=',', usecols=colnames)
walkDataKenneth2 = pd.read_csv('data/test_walk_Kennethdata2.csv', sep=',', usecols=colnames)

standData3 = pd.read_csv('data/test_stand3.csv', sep=',', usecols=colnames)

standData4 = pd.read_csv('data/test_stand4.csv', sep=',', usecols=colnames)

sitData3 = pd.read_csv('data/test_sit3.csv', sep=',', usecols=colnames)

standData5 = pd.read_csv('data/test_stand5.csv', sep=',', usecols=colnames)

dataSets = [sitData, standData, walkData, sitDataKenneth, standDataKenneth, walkDataKenneth]

# combining data
combinedSitData = pd.concat([sitData, sitDataKenneth, sitDataKenneth2, sitData3])
combinedStandData = pd.concat([standData, standDataKenneth, standDataKenneth2, standData3, standData4])
combinedWalkData = pd.concat([walkData, walkDataKenneth, walkDataKenneth2])

combinedData = [combinedSitData, combinedStandData, combinedWalkData]

# computing energy and adding it to data
combinedSitData['energy'] = calcEnergy(combinedSitData)
combinedStandData['energy']  = calcEnergy(combinedStandData)
combinedWalkData['energy'] = calcEnergy(combinedWalkData)

# deletes columns that are not needed
# delColnames = ['timestamp', 'accx', 'accy', 'accz']
# delColnames = ['timestamp', 'energy']
delColnames = ['timestamp']
# # delColnames = ['timestamp', 'energy', 'Pitch_sensor1']
deleteColumns(combinedSitData, delColnames)
deleteColumns(combinedStandData, delColnames)
deleteColumns(combinedWalkData, delColnames)

# combing datasets together
motionDataset = pd.concat(combinedData)

# create target values
targetPair = {0 : 'sit', 1 : 'stand', 2 : 'walk'}
sitDataTarget = createTarget(combinedSitData, 0)
standDataTarget = createTarget(combinedStandData, 1)
walkDataTarget = createTarget(combinedWalkData, 2)
target = sitDataTarget + standDataTarget + walkDataTarget
targetNames = [targetPair[x] for x in target]
nSamples = len(target)

# some plotting
# truncatedWalkData = combinedWalkData[:len(sitData)]
# x = truncatedWalkData['timestamp']
# y = truncatedWalkData['energy']
# plt.plot(x, y)
# plt.show()