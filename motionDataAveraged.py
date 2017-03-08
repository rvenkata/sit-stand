import motionData as md
from utils import *
import matplotlib.pyplot as plt


# computing mean values in intervals
timeSampleRate = 0.5
sitData = createIntervalDataset(md.sitData, timeSampleRate)
standData = createIntervalDataset(md.standData, timeSampleRate)
walkData = createIntervalDataset(md.walkData, timeSampleRate)
sitDataKenneth = createIntervalDataset(md.sitDataKenneth, timeSampleRate)
standDataKenneth = createIntervalDataset(md.standDataKenneth, timeSampleRate)
walkDataKenneth = createIntervalDataset(md.walkDataKenneth, timeSampleRate)

# combining data together
combinedSitData = pd.concat([sitData, sitDataKenneth])
combinedStandData = pd.concat([standData, standDataKenneth])
combinedWalkData = pd.concat([walkData, walkDataKenneth])

combinedData = [combinedSitData, combinedStandData, combinedWalkData]

# computing and adding energy column
combinedSitData['energy'] = calcEnergy(combinedSitData)
combinedStandData['energy']  = calcEnergy(combinedStandData)
combinedWalkData['energy'] = calcEnergy(combinedWalkData)

# deletes columns that are not needed
# using energy with pitch
delColnames = ['timestamp', 'accx', 'accy', 'accz']
# using raw acceleration only
# delColnames = ['timestamp', 'energy', 'Pitch_sensor1']
# using acceleration and pitch
# delColnames = ['timestamp', 'energy']
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

# plotting data
# truncatedWalkData = combinedWalkData[:300]
# x = truncatedWalkData['timestamp']
# y = truncatedWalkData['accz']
# plt.plot(x, y)
# plt.show()