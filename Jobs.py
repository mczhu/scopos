import unirest
import urllib2
import numpy as np
from bs4 import BeautifulSoup
from collections import namedtuple
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models, similarities
import pymysql as mdb
from datetime import datetime
import os.path
from wordcloud import WordCloud
from itertools import chain
import pickle

import pdb

class Jobs(object):
    
    MAX_JOBS_PER_QUERY = 10
    STOPLIST = set('for a an of the and to in at with'.split())

    def __init__(self, dbUsr = 'mengchen', dbPsw = '', dbName = 'indeed'):
        self.jobs = []
        self.stemmer = PorterStemmer()
        # self._corpus_lsi = None
        if os.path.isfile('jobs.dict'):
            self._dictionary = corpora.Dictionary.load('jobs.dict')
        else:
            self._dictionary = None
        if os.path.isfile('model.lda'):
            self._lda = models.LdaModel.load('model.lda')
        else:
            self._lda = None
        if os.path.isfile('model.lsi'):
            self._lsi = models.LsiModel.load('model.lsi')
        else:
            self._lsi = None
        if os.path.isfile('transform.tfidf'):
            self._tfidf = models.TfidfModel.load('transform.tfidf')
        else:
            self._tfidf = None
        if os.path.isfile('jobCorpus.mm'):
            self._corpus_tfidf = corpora.MmCorpus('jobCorpus.mm')
        else:
            self._corpus_tfidf = None
        if os.path.isfile('similarity.index'):
            self._simIndex = similarities.MatrixSimilarity.load('similarity.index')
        else:
            self._simIndex = None
        if os.path.isfile('vec.rep'):
            self._vecRep = pickle.load(open('vec.rep', 'rb'))
        else:
            self._vecRep = None
        self._con = mdb.connect('localhost', dbUsr, dbPsw, dbName, charset='utf8')
        self._index = None
        self._update_index()


    def getJob(self, index):
        with self._con:
            cur = self._con.cursor()
            sql = "SELECT * FROM Jobs WHERE `jobkey` = %s"
            # sql = "SELECT * FROM SE WHERE `jobkey` = %s"            
            cur.execute(sql, (self._index[index]))
            rows = cur.fetchall()
        if not rows:
            return None
        Job = namedtuple('Job', ['jobkey', 'title', 'company', 'location', 'url', 'date', 'summary',  'query' ])
        Job.title = rows[0][0]
        Job.company = rows[0][1]
        Job.location = rows[0][2]
        Job.url = rows[0][3]
        Job.query = rows[0][4]
        Job.summary = rows[0][5]
        Job.html = rows[0][6]
        Job.jobkey = rows[0][7]
        Job.date = rows[0][8]
        return Job
        
    def addToDB(self, publisher_key, mashapeKey, query="machine+learning", location="New+York%2C+NY", nJobs=25):
        for queryIdx in range((nJobs-1)/Jobs.MAX_JOBS_PER_QUERY+1):
            response = unirest.get("https://indeed-indeed.p.mashape.com/apisearch?publisher={}&callback=<required>&chnl=<required>&co=<required>&filter=1&format=json&fromage=<required>&highlight=<required>&jt=<required>&l={}&latlong=<required>&limit={}&q={}&radius=25&sort=<required>&st=<required>&start={}&useragent=<required>&userip=<required>&v=2".format(publisher_key, location, Jobs.MAX_JOBS_PER_QUERY, query, queryIdx*Jobs.MAX_JOBS_PER_QUERY),
      headers={
        "X-Mashape-Key": mashapeKey,
        "Accept": "application/json"
      }
    )

            # scrape the job page
            for idx, result in enumerate(response.body['results']):
                print('Parsing job {}'.format(idx))

                site_url = result['url']
                html = urllib2.urlopen(site_url).read().decode('utf-8')
                soup = BeautifulSoup(html)

                date = datetime.strptime(result['date'], '%a, %d %b %Y %H:%M:%S GMT')

                jobSummary = soup.find_all(class_="summary")[0]
                with self._con:
                    cur = self._con.cursor()
                    sql = "INSERT IGNORE INTO `Jobs` (`jobkey`, `title`, `company`, `location`, `url`, `date`, `summary`, `html`, `query`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    # sql = "INSERT IGNORE INTO `SE` (`jobkey`, `title`, `company`, `location`, `url`, `date`, `summary`, `html`, `query`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

                    cur.execute(sql, (result['jobkey'], result['jobtitle'], result['company'], result['formattedLocation'], result['url'], date.strftime("%Y-%m-%d %H:%M:%S"), jobSummary.get_text(" "), unicode(str(jobSummary), "utf-8"), query))

        self._update_index()

            # # TODO: Sequentially update the model
            # self._init_model(num_topics=5, isInitCorpus=True)

    def genWordCloud(self, query="data+scientist"):
        with self._con:
            cur = self._con.cursor()
            sql = "SELECT `summary` FROM Jobs WHERE query=%s"
            # sql = "SELECT `summary` FROM SE WHERE query=%s"
            cur.execute(sql, (query))
            rows = cur.fetchall()
        # pdb.set_trace()
        
        texts = [[w.lower() for w in word_tokenize(row[0]) if (w.isalpha() and (w not in self.STOPLIST))] for row in rows]
        texts = " ".join(list(chain(*texts)))

        wordcloud = WordCloud().generate(texts)
        return wordcloud

    def removeExpired(self, indeedKey, mashapeKey):
        with self._con:
            cur = self._con.cursor()
            cur.execute("SELECT jobkey FROM Jobs")
            for row in cur:
                # Get the expired status
                response = unirest.get("https://indeed-indeed.p.mashape.com/apigetjobs?publisher={}&format=json&jobkeys={}&v=2".format(indeedKey, row[0]),  headers={
    "X-Mashape-Key": mashapeKey,
    "Accept": "application/json"
  }
)
                if (response.body["results"]):
                    if (not response.body["results"][0]["expired"]):
                        continue

                print ("Processing Job " + row[0])
                sql = "INSERT IGNORE OldJobs SELECT * FROM Jobs WHERE `jobkey`=%s"
                cur2 = self._con.cursor()
                cur2.execute(sql, row[0])
                sql = "DELETE IGNORE FROM Jobs WHERE  `jobkey`=%s"
                cur2.execute(sql, row[0])

    def _import_text(self):
        with self._con:
            cur = self._con.cursor()
            cur.execute("SELECT `summary` FROM Jobs")
            rows = cur.fetchall()
        
        texts = [[w.lower() for w in word_tokenize(row[0]) if (w.isalpha() and (w not in self.STOPLIST))] for row in rows]


        # remove words that appear only once
        all_tokens = sum(texts, [])
        tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)
        texts = [[self.stemmer.stem(word) for word in text if word not in tokens_once] for text in texts]

        return texts
                
    def _prepare_corpus(self):
        texts = self._import_text()
        
        # Convert into BOW
        self._dictionary = corpora.Dictionary(texts)
        self._dictionary.save('jobs.dict')
        
        corpus = [self._dictionary.doc2bow(text) for text in texts]

        # Transformation
        self._tfidf = models.TfidfModel(corpus)
        self._tfidf.save('transform.tfidf')
        self._corpus_tfidf = self._tfidf[corpus]
        corpora.MmCorpus.serialize('jobCorpus.mm', self._corpus_tfidf)
            
    def _init_lsi(self, num_topics=2):
        self._lsi =  models.LsiModel(self._corpus_tfidf, id2word=self._dictionary, num_topics=num_topics)
        self._lsi.save('model.lsi')

        self._vecRep = [vecRep for vecRep in self._lsi[self._corpus_tfidf]]
        with open('vec.rep','w') as f:
            pickle.dump(self._vecRep, f)


    def _init_model(self, num_topics=5, isInitCorpus=False):
        if isInitCorpus:
            self._prepare_corpus()
        self._init_lsi(num_topics = num_topics)
        self._simIndex = similarities.MatrixSimilarity(self._lsi[self._corpus_tfidf])
        self._simIndex.save('similarity.index')
        self._update_index()

        
    def _update_index(self):
        with self._con:
            cur = self._con.cursor()
            cur.execute("SELECT `jobkey` FROM Jobs")
            rows = cur.fetchall()

        self._index = [row[0] for row in rows]

    def _findSimilarFromVec(self, jobVec, top=10, exclude=[]):
        # Find similar jobs from internal vector space representation
        sim_index = self._simIndex[jobVec]
        sim_index[exclude] = np.NINF
        topInd = np.argsort(sim_index)[::-1][:top]
        return topInd, sim_index
        
        
    def findSimilarFromVec(self, jobVec, top=10, exclude=[]):
        # Find similar jobs with  numpy vector space representation
        jobVecInternal = [(i, vec) for (i, vec) in enumerate(jobVec.tolist())]
        return self._findSimilarFromVec(jobVecInternal, top=top, exclude=exclude)
                           
        
    def findSimilar(self, jobDescription, top=10, exclude=[]):
        topInd, sim_index = self._findSimilarFromVec(self._getVecRep(jobDescription), top=top, exclude=exclude)
        return topInd, sim_index

    def findJobsInSameCompany(self, ind):
        # return the index of jobs from the same company
        with self._con:
            cur = self._con.cursor()
            sql = "SELECT `jobkey` from Jobs WHERE `company` = %s"
            cur.execute(sql, (self.getJob(ind).company))
            rows = cur.fetchall()
            indSameCompany = [self._index.index(row[0]) for row in rows]
            indSameCompany.remove(ind)
            return indSameCompany
        
    def print_topics(self, num_topics=5):
        self._lsi.print_topics(num_topics=num_topics)

    def getVecRepMat(self):
        # Convert the vector representation of the corpus to a numpy array
        return np.array([[vecRepEntry[1] for vecRepEntry in vecRep] for vecRep in self._vecRep])

    def _getVecRep(self, jobDescription):
        if self._lsi is None or self._tfidf is None or self._simIndex is None or self._dictionary is None:        
            self._init_model()
        text = [self.stemmer.stem(w.lower()) for w in word_tokenize(jobDescription) if (w.isalpha() and (w not in self.STOPLIST))]
        vec_bow = self._dictionary.doc2bow(text)
        vec_tfidf = self._tfidf[vec_bow]
        vec_lsi = self._lsi[vec_tfidf]
        return vec_lsi

    def getVecRep(self, jobDescription):
        # Convert the vector space representation of a job description to a numpy array
        vec_lsi = self._getVecRep(jobDescription)
        return np.array([vecRep[1] for vecRep in self._getVecRep(jobDescription)])

    def connect(self, dbUsr = 'mengchen', dbPsw = '', dbName = 'indeed'):
        self._con = mdb.connect('localhost', dbUsr, dbPsw, dbName, charset='utf8')

    # def _view_topics_scatter(self):
    #     #  obsolete
    #     if self._corpus_lsi is None:
    #         self._init_lsi()
    #     fig, ax = plt.subplots(subplot_kw=dict(axisbg='#EEEEEE'))
    #     categories = np.unique([job.query for job in self.jobs])
    #     colors = np.linspace(0, 1, len(categories))
    #     colordict = dict(zip(categories, colors))
    #     jobColors = [colordict[job.query] for job in self.jobs]
    #     # Measure the cosine distance to reference
    #     distToReference = [np.inner(np.array([doc[0][1], doc[1][1]]), np.array([0, 1]))  for doc in self._corpus_lsi]
    #     scatter = ax.scatter(distToReference, np.zeros(len(distToReference)), c=jobColors,
    #                s=50, cmap=plt.cm.jet)
    #     labels = ["{}:".format(idx)+job.company  for idx, job in enumerate(self.jobs)]
    #     ax.grid(color='white', linestyle='solid')
    #     ax.set_title("Jobs topic space", size=20)
    #     ax.legend()
    #     # tooltip = mpld3.plugins.PointLabelTooltip(scatter, labels=labels)
    #     # mpld3.plugins.connect(fig, tooltip)
    #     # mpld3.show()
