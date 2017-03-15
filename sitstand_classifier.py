import pandas as pd
import numpy as np
from sklearn import svm, metrics
from math import sqrt
import matplotlib.pyplot as plt
from matplotlib.pyplot import plot, draw, show



def calc_energy(data):
    energy_column = []
    for i in range(0, len(data)):
        row = data.values[i]
        accx = row[1]
        accy = row[2]
        accz = row[3]
        energy = (accx ** 2 + accy ** 2 + accz ** 2)
        energy_column.append(energy)
    return energy_column

def delete_columns(data, columns):
    for col in columns:
        del data[col]

def create_target(data, target_value):
    target = []
    for i in range(0, len(data)):
        target.append(target_value)
    return target

colnames = ['Pitch_sensor1', 'accx', 'accy', 'accz']
sit_data = pd.read_csv('data/test_sit.csv', sep=',', usecols=colnames)
stand_data = pd.read_csv('data/test_stand.csv', sep=',', usecols=colnames)
walk_data = pd.read_csv('data/test_walk.csv', sep=',', usecols=colnames)
sit_dataKenneth = pd.read_csv('data/test_sit_Kennethdata.csv', sep=',', usecols=colnames)
stand_dataKenneth = pd.read_csv('data/test_stand_Kennethdata.csv', sep=',', usecols=colnames)
walk_dataKenneth = pd.read_csv('data/test_walk_Kennethdata.csv', sep=',', usecols=colnames)

sit_data = pd.concat([sit_data, sit_dataKenneth])
stand_data = pd.concat([stand_data, stand_dataKenneth])
walk_data = pd.concat([walk_data, walk_dataKenneth])

# add energy column
sit_data['energy'] = calc_energy(sit_data)
stand_data['energy']  = calc_energy(stand_data)
walk_data['energy'] = calc_energy(walk_data)


# deletes columns that are not needed
del_colnames = colnames[1:]
delete_columns(sit_data, del_colnames)
delete_columns(stand_data, del_colnames)
delete_columns(walk_data, del_colnames)

# combing datasets together
frames = [sit_data, stand_data, walk_data]
motion_data = pd.concat(frames)
print("length of sit_data")
print(sit_data.shape)
print("length of stand_data")
print(stand_data.shape)
print("length of walk_data")
print(walk_data.shape)
print("length of motion_data")
print(motion_data.shape)

# create target values
target_pair = {0 : 'sit', 1 : 'stand', 2 : 'walk'}
sit_data_target = create_target(sit_data, 0)
stand_data_target = create_target(stand_data, 1)
walk_data_target = create_target(walk_data, 2)
target = sit_data_target + stand_data_target + walk_data_target
target_names = [target_pair[x] for x in target]
n_samples = len(target)

# plt.plot(target)
# plt.title('0-sit, 1-stand,2-walk')
# plt.ylim(0,4)
# show()

# train an SVM model
X, y = motion_data.values, target_names

clf = svm.SVC()
from sklearn.cross_validation import train_test_split
Xtrain, Xtest, ytrain, ytest = train_test_split(X, y)
clf.fit(Xtrain, ytrain)
ypred = clf.predict(Xtest)
# cross validation
print ("******results for standard SVM******")
print (metrics.classification_report(ytest, ypred))
print (metrics.confusion_matrix(ytest, ypred))

# use random forrest instead
from sklearn.ensemble import RandomForestClassifier
clf = RandomForestClassifier(n_estimators=100, random_state=0)
clf.fit(Xtrain, ytrain)
ypred = clf.predict(Xtest)
#plt.plot(ypred)
#show()
print ("******results for standard random forrest******")
print (metrics.classification_report(ytest, ypred))
print (metrics.confusion_matrix(ytest, ypred))

from sklearn.externals import joblib
joblib.dump(clf, 'rf_classifier.pkl') 

import _pickle as cPickle
with open('C:\\Anaconda3\\rf_classifier2', 'wb') as f:
    cPickle.dump(clf, f)


with open('C:\\Anaconda3\\rf_classifier2', 'rb') as f:
    rf = cPickle.load(f)

preds = rf.predict(Xtest)
print ("******results for standard Pickle random forrest ******")
print (metrics.classification_report(ytest, preds))
print (metrics.confusion_matrix(ytest, preds))

