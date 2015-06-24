from __future__ import division
import numpy as np
import matplotlib.pyplot as plt

class PrecisionRecall(object):
    def __init__(self, relevant, retrieved, numRelevant):
        # List of retrieved items
        self.retrieved = retrieved
        # relevant item string
        self.relevant = relevant
        # Total number of relevant items
        self.numRelevant = numRelevant
        self.precision = np.empty(len(retrieved))
        self.recall = np.empty(len(retrieved))

    def precisionRecall(self):
        truePositives = np.cumsum(np.array([self.relevant==element for element in self.retrieved]).astype(int))
        falsePositives = np.cumsum(np.array([self.relevant!=element for element in self.retrieved]).astype(int))
        self.precision = truePositives / (truePositives + falsePositives)
        self.recall = truePositives / self.numRelevant

    def plot(self):
        self.precisionRecall() 
        plt.plot(self.recall, self.precision, '-x')
        plt.xlim([0, 1.0])
        plt.ylim([0, 1.1])
        plt.xlabel("Recall")
        plt.ylabel("Precision")
        plt.show()
