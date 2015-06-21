from Jobs import Jobs
import matplotlib.pyplot as plt

if __name__ == '__main__':
    # Test search
    jobs = Jobs()

    with open("indeed_api_key") as f:
        indeedKey = f.read()
    jobs.addToDB(indeedkey, "data+engineer",  nJobs=500)
    # jobs.search()

    # TODO: check that the returned jobs are indeed close to the query by visualizing the scatter

    # jobs.view_topics_scatter()

    # jobs.print_topics()

    # Job = jobs.getJob(2)
    # # jobs.view_jobs(queryJobIdx)
    # simInd, simVal = jobs.findSimilar(Job.summary)
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
