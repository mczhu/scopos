import numpy as np
import pdb

class Rocchio(object):
    # Rocchio's algorithm for relevance feedback
    ALPHA = 1
    BETA = .75
    GAMMA = .15

    def __init__(self, vecRep, initQuery, relevant=[], irrelevant=[]):
        # old_err_state = np.seterr(divide='raise')
        self._vecRep = vecRep
        self._initQuery = initQuery
        self._relevant = relevant
        self._irrelevant = irrelevant

    def _getNewQuery(self):
        sumRel = 0
        if len(self._relevant) != 0:
            sumRel = self.BETA * np.sum(np.array([self._vecRep[ind] for ind in self._relevant]), axis=0) / len(self._relevant)
        sumIrrel = 0
        if len(self._irrelevant) != 0:
            sumIrrel = self.GAMMA * np.sum(np.array([self._vecRep[ind] for ind in self._irrelevant]), axis=0) / len(self._irrelevant)
        # pdb.set_trace()
        return self.ALPHA * self._initQuery + sumRel - sumIrrel
    
    def addToRelevant(self, jobInd):
        # Add the document to the "relevant" class
        self._relevant = self._relevant + [jobInd]
        return self._getNewQuery()

    def addToIrrelevant(self, jobInd):
        # Add the document to the "relevant" class
        self._irrelevant = self._irrelevant + [jobInd]
        return self._getNewQuery()

    def getRelevant(self):
        return self._relevant

    def getIrrelevant(self):
        return self._irrelevant
