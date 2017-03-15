import motionDataAveraged as md
from sklearn import svm, metrics
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import train_test_split
from sklearn.externals import joblib

# using moving average dataset
X, y = md.motionDataset, md.targetNames
Xtrain, Xtest, ytrain, ytest = train_test_split(X, y)
clf = RandomForestClassifier(n_estimators=100, random_state=0)
clf.fit(Xtrain, ytrain)
ypred = clf.predict(Xtest)

# cross validation
print ("******results for standard random forrest******")
print (metrics.classification_report(ytest, ypred))
print (metrics.confusion_matrix(ytest, ypred))

# re-train using the entire dataset
clf = RandomForestClassifier(n_estimators=100, random_state=0)
clf.fit(X, y)

joblib.dump(clf, 'model/rf_classifier.pkl') 