import motionDataAveraged as md
from sklearn import svm, metrics
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import train_test_split
from sklearn.externals import joblib

# using moving average dataset
X, y = md.motionDataset, md.targetNames

# re-train using the entire dataset
clf = RandomForestClassifier(n_estimators=100, random_state=0)
clf.fit(X, y)

x = md.combinedStandData
print(clf.predict(x))
joblib.dump(clf, 'model/rf_classifier.pkl') 

clf2 = joblib.load('model/rf_classifier.pkl')
print(clf2.predict(x))