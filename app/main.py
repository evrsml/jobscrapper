from flask import Flask, render_template, request, redirect, send_file 

from parser_hh import get_jobs

from parser_so import get_jobs_so

from exporter import save_to_csv

app = Flask('JobScrapper')

db = {}


@app.route('/')
def home():
  return render_template('home.html')

@app.route('/report')
def report():
  keyword = request.args.get('keyword')
  if keyword  is not None:
    keyword = keyword.lower()
    getDB = db.get(keyword)
    if getDB:
      jobs = getDB
    else: 
      jobs = get_jobs(keyword)
      db[keyword] = jobs
    print(jobs)
  else:
    return redirect('/')
  return render_template("report.html", searchBy=keyword, resultsNumber=len(jobs), jobs = jobs)

@app.route('/report2')
def report2():
  keyword = request.args.get('keyword')
  if keyword  is not None:
    keyword = keyword.lower()
    getDB = db.get(keyword)
    if getDB:
      jobs = getDB
    else: 
      jobs = get_jobs_so(keyword)
      db[keyword] = jobs
    print(jobs)
  else:
    return redirect('/')
  return render_template("report.html", searchBy=keyword, resultsNumber=len(jobs), jobs = jobs)

@app.route('/export')
def export():
  try:
    keyword = request.args.get('keyword')
    if not keyword:
      raise Exception()
    keyword = keyword.lower()
    jobs = db.get(keyword)
    if not jobs:
      raise Exception()
    save_to_csv(jobs)
    return send_file('jobs.csv')
  except:
    return redirect('/')

app.run(host="0.0.0.0")
