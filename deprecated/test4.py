import pandas as pd
from sklearn.externals import joblib
from utils import * 

colnames = ['timestamp', 'Pitch_sensor1', 'accx', 'accy', 'accz']
def prepDataForClassification(dataset):
    dataset['energy'] = calcEnergy(dataset)
    dataset = createMovingIntervalDataset(dataset, 0.5)
    delColnames = ['timestamp']
    deleteColumns(dataset, delColnames)
    return dataset

standData = pd.read_csv('sit3.csv', sep=',', usecols=colnames)
standData = prepDataForClassification(standData)
clf = joblib.load('model/rf_classifier.pkl') 
print(clf.predict(standData))


