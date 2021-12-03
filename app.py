from main import *
from flask import Flask, request, jsonify

from markupsafe import escape

import base64
from io import BytesIO

from matplotlib.figure import Figure
import numpy as np


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

@app.route('/showActors/<username>/<reponame>')
def showActors(username,reponame):
    offset  = request.args.get('offset', default=365*24*60, type=int)

    events = fetchEvents(username, reponame)
    E = eventActors(events,offset)

    # Generate the figure **without using pyplot**.
    fig = Figure()
    ax = fig.subplots()

    data = E.values()
    ind = np.arange(len(data))    # the x locations for the groups
    p1 = ax.bar(ind, data, 0.35)

    ax.axhline(0, color='grey', linewidth=0.8)
    ax.set_ylabel('Created Events')
    ax.set_title('Number of events by user')
    ax.set_xticks(ind)
    ax.set_xticklabels(E.keys(), rotation=10)

    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"
