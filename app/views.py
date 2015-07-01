from flask import render_template, request, session
from app import app
import pymysql as mdb
from Rocchio import Rocchio

import sys
import pdb

@app.route('/')
@app.route('/index')
def index():
    jobDescription = request.args.get('jobDescription')
    session['checked'] = request.args.get('checked')
    global rocchio
    session['sameCompany'] = []

    if jobDescription is None:
        jobsList = []
        jobDescription = "data scientist"
        sim_score_sorted = ""
        session['checked'] = "checked"
    else:
        rocchio = Rocchio(app.jobs.getVecRepMat(), app.jobs.getVecRep(jobDescription))
        simInd, sim_score = app.jobs.findSimilar(jobDescription)
        sim_score_sorted = [sim_score[i] for i in simInd]
        jobsList = [app.jobs.getJob(ind) for ind in simInd]
        session['jobInd'] = simInd[0]
    return render_template("index.html", jobsList = jobsList, jobDescription = jobDescription, sim_score = sim_score_sorted, checked = session['checked'])

@app.route('/search')
def search():
    jobDescription = request.args.get('jobDescription')

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
    global rocchio
    newQuery = rocchio.addToRelevant(session['jobInd'])
    if session['checked']:
        session['sameCompany'] = session['sameCompany'] + app.jobs.findJobsInSameCompany(session['jobInd'])
    topInd, simVal = app.jobs.findSimilarFromVec(newQuery, top=1, exclude=rocchio.getRelevant()+rocchio.getIrrelevant()+session['sameCompany'])
    session['jobInd'] = topInd[0]
    return render_template("like.html", topJob=app.jobs.getJob(session['jobInd']))

@app.route('/dislike')
def dislike():
    global rocchio
    newQuery = rocchio.addToIrrelevant(session['jobInd'])
    topInd, simVal = app.jobs.findSimilarFromVec(newQuery, top=1, exclude=rocchio.getRelevant()+rocchio.getIrrelevant()+session['sameCompany'])
    session['jobInd'] = topInd[0]
    return render_template("dislike.html", topJob=app.jobs.getJob(session['jobInd']))
    
@app.route('/viewliked')
def viewliked():
    global rocchio
    jobsList = [app.jobs.getJob(ind) for ind in rocchio.getRelevant()]
    return render_template("viewliked.html", jobsList=jobsList)
    
