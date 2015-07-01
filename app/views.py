from flask import render_template, request
from app import app
import pymysql as mdb
from Rocchio import Rocchio

import sys
import pdb

@app.route('/')
@app.route('/index')
def index():
    jobDescription = request.args.get('jobDescription')
    global checked
    checked = request.args.get('checked')
    global rocchio
    global jobInd
    global sameCompany
    sameCompany = []

    if jobDescription is None:
        jobsList = []
        jobDescription = "data scientist"
        sim_score_sorted = ""
        checked = "checked"
    else:
        # jobs = Jobs()
        rocchio = Rocchio(app.jobs.getVecRepMat(), app.jobs.getVecRep(jobDescription))
        simInd, sim_score = app.jobs.findSimilar(jobDescription)
        sim_score_sorted = [sim_score[i] for i in simInd]
        jobsList = [app.jobs.getJob(ind) for ind in simInd]
        jobInd = simInd[0]
    return render_template("index.html", jobsList = jobsList, jobDescription = jobDescription, sim_score = sim_score_sorted, checked = checked)

@app.route('/search')
def search():
    jobDescription = request.args.get('jobDescription')
    # TODO: instead of global variables, use flask session and define own JSON conversion

    if jobDescription is None:
        jobsList = []
        jobDescription = ""
        sim_score_sorted = ""
    else:
        simInd, sim_score = app.jobs.findSimilar(jobDescription)
        sim_score_sorted = [sim_score[i] for i in simInd]
        jobsList = [app.jobs.getJob(ind) for ind in simInd]
    return render_template("search.html", jobsList = jobsList, jobDescription = jobDescription, sim_score = sim_score_sorted)


@app.route('/like')
def like():
    global jobInd
    global rocchio
    # global jobs
    global sameCompany
    newQuery = rocchio.addToRelevant(jobInd)
    global checked
    # checked = request.args.get('checked')
    if checked:
        sameCompany = sameCompany + app.jobs.findJobsInSameCompany(jobInd)
    topInd, simVal = app.jobs.findSimilarFromVec(newQuery, top=1, exclude=rocchio.getRelevant()+rocchio.getIrrelevant()+sameCompany)
    jobInd = topInd[0]
    return render_template("like.html", topJob=app.jobs.getJob(jobInd))

@app.route('/dislike')
def dislike():
    global jobInd
    global rocchio
    # global jobs
    global sameCompany
    global checked
    # checked = request.args.get('checked')
    newQuery = rocchio.addToIrrelevant(jobInd)
    topInd, simVal = app.jobs.findSimilarFromVec(newQuery, top=1, exclude=rocchio.getRelevant()+rocchio.getIrrelevant()+sameCompany)
    jobInd = topInd[0]
    return render_template("dislike.html", topJob=app.jobs.getJob(jobInd))
    
@app.route('/viewliked')
def viewliked():
    global rocchio
    # global jobs
    jobsList = [app.jobs.getJob(ind) for ind in rocchio.getRelevant()]
    return render_template("viewliked.html", jobsList=jobsList)
    
