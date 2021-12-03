from main import *
from flask import Flask, request, jsonify

from markupsafe import escape

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/avgTime/<username>/<reponame>')
def avgTime(username,reponame):
    events = fetchEvents(username, reponame)
    avg    = averageTime(events)

    if avg == -1:
        return f'Repository {escape(username)}/{escape(reponame)} does not report two PullRequestEvents (the average time cannot be computed).'
    else:
        return f'Average time between pull requests for repository /{escape(username)}/{escape(reponame)} is {escape(avg)} seconds.'

@app.route('/groupEvents/<username>/<reponame>')
def groupEvents(username,reponame):
    offset  = request.args.get('offset', default=365*24*60, type=int)

    events = fetchEvents(username, reponame)
    E = totalEvents(events,offset)

    return jsonify(E)
