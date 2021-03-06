from flask import render_template, request, session
from app import app
import pymysql as mdb
from Rocchio import Rocchio
# import pdb

@app.route('/')
@app.route('/index')
def index():
    app.jobs.connect(dbUsr = 'mengchen', dbPsw = '', dbName = 'indeed')
    
    session['jobDescription'] = request.args.get('jobDescription')
    session['checked'] = request.args.get('checked')
    session['sameCompany'] = []
    session['relevant'] = []
    session['irrelevant'] = []

    isSearchHit = True
    
    if session['jobDescription'] is None:
        jobsList = []
        session['jobDescription'] = "data scientist"
        sim_score_sorted = ""
        session['checked'] = "checked"
    else:
        if (len(app.jobs.getVecRep(session['jobDescription'])) == 0):
            isSearchHit = False
        simInd, sim_score = app.jobs.findSimilar(session['jobDescription'])
        sim_score_sorted = [sim_score[i] for i in simInd]
        jobsList = [app.jobs.getJob(ind) for ind in simInd]
        session['jobInd'] = simInd[0]
    return render_template("index.html", jobsList = jobsList, jobDescription = session['jobDescription'], sim_score = sim_score_sorted, checked = session['checked'], isSearchHit = isSearchHit)

@app.route('/search')
def search():
    app.jobs.connect(dbUsr = 'mengchen', dbPsw = '', dbName = 'indeed')
    session['jobDescription'] = request.args.get('jobDescription')

    if session['jobDescription'] is None:
        jobsList = []
        session['jobDescription'] = ""
        sim_score_sorted = ""
    else:
        simInd, sim_score = app.jobs.findSimilar(session['jobDescription'])
        sim_score_sorted = [sim_score[i] for i in simInd]
        jobsList = [app.jobs.getJob(ind) for ind in simInd]
    return render_template("search.html", jobsList = jobsList, jobDescription = session['jobDescription'], sim_score = sim_score_sorted)


@app.route('/like')
def like():
    session['relevant'] = session['relevant'] + [session['jobInd']]
    rocchio = Rocchio(app.jobs.getVecRepMat(), app.jobs.getVecRep(session['jobDescription']), session['relevant'], session['irrelevant'])
    newQuery = rocchio.addToRelevant(session['jobInd'])
    if session['checked']:
        session['sameCompany'] = session['sameCompany'] + app.jobs.findJobsInSameCompany(session['jobInd'])
    topInd, simVal = app.jobs.findSimilarFromVec(newQuery, top=1, exclude=rocchio.getRelevant()+rocchio.getIrrelevant()+session['sameCompany'])
    session['jobInd'] = topInd[0]
    return render_template("like.html", topJob=app.jobs.getJob(session['jobInd']))

@app.route('/dislike')
def dislike():
    session['irrelevant'] = session['irrelevant'] + [session['jobInd']]
    rocchio = Rocchio(app.jobs.getVecRepMat(), app.jobs.getVecRep(session['jobDescription']), session['relevant'], session['irrelevant'])
    newQuery = rocchio.addToIrrelevant(session['jobInd'])
    if session['checked']:
        session['sameCompany'] = session['sameCompany'] + app.jobs.findJobsInSameCompany(session['jobInd'])
    topInd, simVal = app.jobs.findSimilarFromVec(newQuery, top=1, exclude=rocchio.getRelevant()+rocchio.getIrrelevant()+session['sameCompany'])
    session['jobInd'] = topInd[0]
    return render_template("dislike.html", topJob=app.jobs.getJob(session['jobInd']))
    
@app.route('/viewliked')
def viewliked():
    jobsList = [app.jobs.getJob(ind) for ind in session['relevant']]
    return render_template("viewliked.html", jobsList=jobsList)
    
@app.errorhandler(500)
def internal_error(error):
    return "Sorry, Scopos is down. The administrator has been notified."
