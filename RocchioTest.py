from Rocchio import Rocchio
import numpy as np

if __name__ == '__main__':
    vecRep = np.array([[1, 0], [-1, 0], [0.5, 1]])
    rocchio = Rocchio(vecRep, np.array([2, 0]))

    newQuery = rocchio.addToRelevant(0)
    newQuery = rocchio.addToIrrelevant(1)
    # newQuery = rocchio.addToRelevant(2)    
