from flask import render_template, request
from app import app
import pymysql as mdb
from Jobs import Jobs
from Rocchio import Rocchio

import sys
import pdb

@app.route('/')
@app.route('/index')
def index():
    jobDescription = request.args.get('jobDescription')
    # TODO: instead of global variables, use flask session and define own JSON conversion
    global jobs
    jobs = Jobs()

    if jobDescription is None:
        jobsList = []
        jobDescription = ""
        sim_score_sorted = ""
    else:
        simInd, sim_score = jobs.findSimilar(jobDescription)
        sim_score_sorted = [sim_score[i] for i in simInd]
        jobsList = [jobs.getJob(ind) for ind in simInd]
    return render_template("index.html", jobsList = jobsList, jobDescription = jobDescription, sim_score = sim_score_sorted)


@app.route('/recommend')
def recommend():
    jobDescription = request.args.get('jobDescription')
    isRepeatCompany = request.args.get('repeat')
    global rocchio
    global jobInd
    global jobs
    jobs = Jobs()
    global sameCompany
    sameCompany = []

    if jobDescription is None:
        jobsList = []
        jobDescription = "data scientist"
        sim_score_sorted = ""
    else:
        # jobs = Jobs()
        rocchio = Rocchio(jobs.getVecRepMat(), jobs.getVecRep(jobDescription))
        simInd, sim_score = jobs.findSimilar(jobDescription)
        sim_score_sorted = [sim_score[i] for i in simInd]
        jobsList = [jobs.getJob(ind) for ind in simInd]
        jobInd = simInd[0]
    return render_template("recommend.html", jobsList = jobsList, jobDescription = jobDescription, sim_score = sim_score_sorted)

@app.route('/like')
def like():
    global jobInd
    global rocchio
    global jobs
    global sameCompany
    newQuery = rocchio.addToRelevant(jobInd)
    sameCompany = sameCompany + jobs.findJobsInSameCompany(jobInd)
    topInd, simVal = jobs.findSimilarFromVec(newQuery, top=1, exclude=rocchio.getRelevant()+rocchio.getIrrelevant()+sameCompany)
    jobInd = topInd[0]
    return render_template("like.html", topJob=jobs.getJob(jobInd))

@app.route('/dislike')
def dislike():
    global jobInd
    global rocchio
    global jobs
    global sameCompany
    # rocchio = request.args.get('rocchio')
    newQuery = rocchio.addToIrrelevant(jobInd)
    topInd, simVal = jobs.findSimilarFromVec(newQuery, top=1, exclude=rocchio.getRelevant()+rocchio.getIrrelevant()+sameCompany)
    jobInd = topInd[0]
    return render_template("dislike.html", topJob=jobs.getJob(jobInd))
    
@app.route('/viewliked')
def viewliked():
    global rocchio
    global jobs
    jobsList = [jobs.getJob(ind) for ind in rocchio.getRelevant()]
    return render_template("viewliked.html", jobsList=jobsList)
    
