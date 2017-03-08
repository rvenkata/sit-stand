import motionDataAveraged as md
from sklearn import svm, metrics

# train an SVM model
X, y = md.motionDataset, md.targetNames
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
print ("******results for standard random forrest******")
print (metrics.classification_report(ytest, ypred))
print (metrics.confusion_matrix(ytest, ypred))

# print("Classification report for classifier %s:\n%s\n"
#       % (clf, metrics.classification_report(expected, predicted)))
# print("Confusion matrix:\n%s" % metrics.confusion_matrix(expected, predicted))



