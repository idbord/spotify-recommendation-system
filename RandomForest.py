import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

class RandomForest:
    def __init__(self, n_trees):# classifier = RandomForestClassifier(n_estimators=n_trees)
        self.classifier = RandomForestClassifier(n_estimators=n_trees)

    def fitLocal(self, x_train, y_train):# classifier.fit(X_train, y_train)
        self.classifier.fit(x_train, y_train)

    def prediction(self, x_test):# label_prediction = clf.predict(X_test)
        return self.classifier.predict(x_test)