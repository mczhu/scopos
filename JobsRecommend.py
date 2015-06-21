from Jobs import Jobs
from Rocchio import Rocchio

def addToIrrelevant(rocchio, jobs, topInd):
    newQuery = rocchio.addToIrrelevant(topInd[0])
    topInd, simVal = jobs.findSimilarFromVec(newQuery, top=1, exclude=rocchio.getRelevant()+rocchio.getIrrelevant())
    topJob = jobs.getJob(topInd[0])
    print(topJob.jobkey)
    print(topJob.title)
    print(topJob.summary)
    print('\n')
    return topInd

def addToRelevant(rocchio, jobs, topInd):
    newQuery = rocchio.addToRelevant(topInd[0])
    topInd, simVal = jobs.findSimilarFromVec(newQuery, top=1, exclude=rocchio.getRelevant()+rocchio.getIrrelevant())
    topJob = jobs.getJob(topInd[0])
    print(topJob.jobkey)
    print(topJob.title)
    print(topJob.summary)
    print('\n')
    return topInd

if __name__ == '__main__':
    # Test job recommendation
    jobs = Jobs()
    query = "data scientist"
    rocchio = Rocchio(jobs.getVecRepMat(), jobs.getVecRep(query))
    topInd, simVal = jobs.findSimilar(query, top=1)
    topJob = jobs.getJob(topInd[0])
    print(topJob.jobkey)
    print(topJob.title)
    print(topJob.summary)
    print('\n')

    # topInd = addToIrrelevant(rocchio, jobs, topInd)
    # topInd = addToIrrelevant(rocchio, jobs, topInd)
    # topInd = addToIrrelevant(rocchio, jobs, topInd)
    # topInd = addToIrrelevant(rocchio, jobs, topInd)
    # topInd = addToRelevant(rocchio, jobs, topInd)
    # topInd = addToRelevant(rocchio, jobs, topInd)
    # topInd = addToRelevant(rocchio, jobs, topInd)
    # topInd = addToRelevant(rocchio, jobs, topInd)
    # topInd = addToRelevant(rocchio, jobs, topInd)
    # topInd = addToIrrelevant(rocchio, jobs, topInd)
    # topInd = addToIrrelevant(rocchio, jobs, topInd)                
        
