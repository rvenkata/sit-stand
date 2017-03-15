import csv
from sklearn.externals import joblib
from math import sqrt

clf = joblib.load('model/rf_classifier.pkl')
data = [919.5965576171875,0.5539054274559021,0.003994387108832598,0.22452613711357117,0.8017237782478333,128.0,-14.023963928222656,22.063684463500977,-0.1206054836511612,-0.0449218787252903,0.9936524629592896,5.18798828125,-3.204345703125,-2.593994140625,3.317595958709717]

energy = sqrt(data[8]*data[8] + data[9]*data[9] + data[10]*data[10])
sample = [data[6], data[8], data[9], data[10], energy] 

print(clf.predict(sample))
