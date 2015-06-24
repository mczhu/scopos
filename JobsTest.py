from Jobs import Jobs
import matplotlib.pyplot as plt
import PrecisionRecall

if __name__ == '__main__':
    # Test search
    jobs = Jobs()

    with open("indeed_api_key") as f:
        indeedKey = f.read()
    jobs.addToDB(indeedKey, "housekeeper",  nJobs=10)
    jobs._init_model(num_topics=50, isInitCorpus=True)

    # jobs.search()

    # TODO: check that the returned jobs are indeed close to the query by visualizing the scatter

    # jobs.view_topics_scatter()

    # jobs.print_topics()

    # Job = jobs.getJob(2)
    # # jobs.view_jobs(queryJobIdx)
    # # simInd, simVal = jobs.findSimilar(Job.summary, exclude=[2, 712])
    # # jobs.view_jobs(simInd[0])
    # # jobs.view_jobs(simInd[1])
    # # jobs.view_jobs(simInd[2])

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

    isPR = True
    if isPR:
        simInd, simVal = jobs.findSimilar("housekeeper", top=10)
        retrieved = [jobs.getJob(ind).query for ind in simInd]
        relevant = "housekeeper"
        pr = PrecisionRecall.PrecisionRecall(relevant, retrieved, 10)
        pr.plot()
        plt.savefig('pr.png')
        
