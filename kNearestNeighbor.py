import numpy as np
from collections import Counter

# TODO Comment this code


def euclideanDistance(x1, x2):  # Calculates euclidean distance based off two input values
    return np.sqrt(np.sum((x1 - x2) ** 2))


class KNN:

    def __init__(self, k):  # initialization
        self.k = k

    def fit(self, trainingSample, trainingClass):  # Collection of training datasets
        self.X_train = trainingSample
        self.Y_train = trainingClass

    def predict(self, testSample):  # Prediction of each member in the test sample
        predicted_labels = [self.predictHelper(x) for x in testSample]
        return np.array(predicted_labels)

    def predictHelper(self, indivSample):  # Helper function for predict
        # Calculate distance
        distances = [euclideanDistance(indivSample, x) for x in self.X_train]

        # Figure out KNN
        k_indices = np.argsort(distances)[0:self.k]
        k_nearest_labels = [self.Y_train[i] for i in k_indices]

        # Popular Vote
        # print(Counter(k_nearest_labels).most_common(1))
        most_common = Counter(k_nearest_labels).most_common(1)
        return most_common[0][0]