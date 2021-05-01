import numpy as np


class NaiveBayes:

    def __init__(self, X, y):
        self.num_examples, self.num_features = X.shape
        self.num_classes = len(np.unique(y))
        self.eps = 1e-6
        self.classes_mean = dict()
        self.classes_var = dict()
        self.classes_prior = dict()

    def fit(self, x, y):

        for c in range(self.num_classes):
            x_c = x[y == c]
            self.classes_mean[str(c)] = np.mean(x_c, axis=0)
            self.classes_var[str(c)] = np.var(x_c, axis=0)
            self.classes_prior[str(c)] = x_c.shape[0] / self.num_examples

    def predict(self, x):
        predict_num_examples, predict_num_features = x.shape
        probability = np.zeros((predict_num_examples, self.num_classes))
        for c in range(self.num_classes):
            prior = self.classes_prior[str(c)]
            probability_c = self.density_function(x, self.classes_mean[str(c)], self.classes_var[str(c)])
            probability[:, c] = probability_c + np.log(prior)

        return np.argmax(probability, 1)

    # Density function based off of Gaussian Naive Bayes implementation
    def density_function(self, x, mean, sigma):
        constant = -self.num_features / 2 * np.log(2 * np.pi) - 0.5 * np.sum(np.log(sigma + self.eps))
        probability = 0.5 * np.sum(np.power(x - mean, 2) / (sigma + self.eps), 1)
        return constant - probability
