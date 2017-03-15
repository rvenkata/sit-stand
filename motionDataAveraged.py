import motionData as md
from utils import *
import matplotlib.pyplot as plt


# computing mean values in intervals
timeSampleRate = 0.5
sitData = createMovingIntervalDataset(md.sitData, timeSampleRate)
standData = createMovingIntervalDataset(md.standData, timeSampleRate)
walkData = createMovingIntervalDataset(md.walkData, timeSampleRate)
sitDataKenneth = createMovingIntervalDataset(md.sitDataKenneth, timeSampleRate)
standDataKenneth = createMovingIntervalDataset(md.standDataKenneth, timeSampleRate)
walkDataKenneth = createMovingIntervalDataset(md.walkDataKenneth, timeSampleRate)
sitDataKenneth2 = createMovingIntervalDataset(md.sitDataKenneth2, timeSampleRate)
standDataKenneth2 = createMovingIntervalDataset(md.standDataKenneth2, timeSampleRate)
walkDataKenneth2 = createMovingIntervalDataset(md.walkDataKenneth2, timeSampleRate)

# combining data together
combinedSitData = pd.concat([sitData, sitDataKenneth, sitDataKenneth2])
combinedStandData = pd.concat([standData, standDataKenneth, standDataKenneth2])
combinedWalkData = pd.concat([walkData, walkDataKenneth, walkDataKenneth2])

combinedData = [combinedSitData, combinedStandData, combinedWalkData]

# computing and adding energy column
combinedSitData['energy'] = calcEnergy(combinedSitData)
combinedStandData['energy']  = calcEnergy(combinedStandData)
combinedWalkData['energy'] = calcEnergy(combinedWalkData)

# deletes columns that are not needed
# using energy with pitch
# delColnames = ['timestamp', 'accx', 'accy', 'accz']
# using raw acceleration only
# delColnames = ['timestamp', 'energy', 'Pitch_sensor1']
# using acceleration and pitch
# delColnames = ['timestamp', 'energy']
delColnames = ['timestamp']
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
