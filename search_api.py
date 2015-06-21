import unirest
import urllib2
import numpy as np
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from collections import namedtuple

# TODO: Load the publisher key and mashape key from an external file. Do not upload this file since it contains the private key.

# API from https://www.mashape.com/indeed/indeed
# These code snippets use an open-source library.
response = unirest.get("https://indeed-indeed.p.mashape.com/apisearch?publisher=***REMOVED***&callback=<required>&chnl=<required>&co=<required>&filter=<required>&format=json&fromage=<required>&highlight=<required>&jt=<required>&l=New+York%2C+NY&latlong=<required>&limit=<required>&q=machine+learning&radius=25&sort=<required>&st=<required>&start=<required>&useragent=<required>&userip=<required>&v=2",
  headers={
    "X-Mashape-Key": "dXuBqlLE3LmshDHVmmi6n4qBOiQop1gnU8mjsnKTy2kHthaQnV",
    "Accept": "application/json"
  }
)

response2 = unirest.get("https://indeed-indeed.p.mashape.com/apisearch?publisher=***REMOVED***&callback=<required>&chnl=<required>&co=<required>&filter=<required>&format=json&fromage=<required>&highlight=<required>&jt=<required>&l=New+York%2C+NY&latlong=<required>&limit=<required>&q=delivery+driver&radius=25&sort=<required>&st=<required>&start=<required>&useragent=<required>&userip=<required>&v=2",
  headers={
    "X-Mashape-Key": "dXuBqlLE3LmshDHVmmi6n4qBOiQop1gnU8mjsnKTy2kHthaQnV",
    "Accept": "application/json"
  }
)

# TODO: pickle the response for reproducible results

# TODO: iterator over the urls

# scrape the job page
Jobs = []
for result in response.body['results']+response2.body['results']:
    site_url = result['url']
    html = urllib2.urlopen(site_url).read().decode('utf-8')
    soup = BeautifulSoup(html)

    # TODO: add try/catch

    Job = namedtuple('Job', ['title', 'company', 'location', 'summary', 'url'])
    Job.title = soup.find_all(class_="jobtitle")[0].get_text()
    Job.company = soup.find_all(class_="company")[0].get_text()
    Job.location = soup.find_all(class_="location")[0].get_text()
    Job.summary = soup.find_all(class_="summary")[0].get_text()
    Job.url = site_url

    Jobs.append(Job)
    
# TODO: Jobs class with a list of Job as the member.
# Jobs.add(site_url): 

# TODO: switch to gensim and use streaming

# TODO: shouldn't matter whether removing stop words because they should be discounted with tfidf? Removing them saves space though
# TODO: remove common words.  Remove non-words such as urls. See how I did it in the NLP class. Keep words such as "C++" intact; see NLTK chap 3.
from nltk.tokenize import word_tokenize
stoplist = set('for a of the and to in at with'.split())
texts = [[w.lower() for w in word_tokenize(Job.summary) if w.isalpha() and w not in stoplist] for Job in Jobs]

# remove words that appear only once
all_tokens = sum(texts, [])
tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)
texts = [[word for word in text if word not in tokens_once] for text in texts]

# Convert into BOW
from gensim import corpora, models, similarities
dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]

# TODO: stem the words.

# Calculate the similarity

# Transformation

tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]

lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=2)
# Let's take a look at the two topics
lsi.print_topics(2)
corpus_lsi = lsi[corpus_tfidf]

for doc in corpus_lsi:
    print(doc)

    
# from sklearn.feature_extraction.text import TfidfVectorizer

# documents = [Job.summary for Job in Jobs]
# # TODO: remove duplicates
# # documents.pop(7)
# tfidf = TfidfVectorizer().fit_transform(documents)
# # no need to normalize, since Vectorizer will return normalized tf-idf
# pairwise_similarity = tfidf * tfidf.T.A
# pairwise_similarity = pairwise_similarity - np.eye(pairwise_similarity.shape[0])

# plt.ion()
# plt.matshow(pairwise_similarity)
# plt.colorbar()


# Find the max similar pair

# Find the min similar pair

# Compare the two

# TODO: LSI transform can be trained online

# TODO: update the projection in real-time 

# TODO: implement query: given one job, what are the similar ones?

# TODO: how to visualize? multi-dimensional scaling?

# Look at a particular job

# import webbrowser
# webbrowser.open_new_tab(Jobs[2].url)
