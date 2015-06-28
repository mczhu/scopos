from Jobs import Jobs
import matplotlib.pyplot as plt
import PrecisionRecall

if __name__ == '__main__':
    # Test search
    jobs = Jobs()

    isAddJobs = False
    if isAddJobs:
        with open("indeed_api_key") as f:
            lines = f.read().splitlines() 
        indeedKey = lines[0]
        mashapeKey = lines[1]
        jobs.addToDB(indeedKey, mashapeKey, "data+scientist",  nJobs=10)

    isInitModel = True
    if isInitModel:
        jobs._init_model(num_topics=50, isInitCorpus=True)

    isTestSimilarity = False
    if isTestSimilarity:
        queryJobIdx = 2
        Job = jobs.getJob(queryJobIdx)
        simInd, simVal = jobs.findSimilar(Job.summary)

    # topInd2, sim_index2 = jobs.findSimilarFromVec(jobs.getVecRep(Job.summary))

    # assert np.array_equal(topInd2, simInd)
    
    # vecRep = jobs.getVecRep("data scientist")


    isViewWordcloud = False
    if isViewWordcloud:
        wordcloud = jobs.genWordCloud(query="data+scientist")
        plt.ion()
        plt.imshow(wordcloud)
        plt.axis("off")
        plt.show()
        plt.savefig('data_scientist.png', bbox_inches='tight', pad_inches=0)

    isPR = False
    if isPR:
        simInd, simVal = jobs.findSimilar("housekeeper", top=10)
        retrieved = [jobs.getJob(ind).query for ind in simInd]
        relevant = "housekeeper"
        pr = PrecisionRecall.PrecisionRecall(relevant, retrieved, 10)
        pr.plot()
        plt.savefig('pr.png')
        
