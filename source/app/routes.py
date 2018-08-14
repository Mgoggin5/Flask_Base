from flask import render_template, flash, redirect, url_for, request, \
    g, jsonify
from redis import Redis, RedisError
import os
import socket
from app import redis, app, mdb

@app.route("/")
def hello():
    try:
        visits = redis.incr("counter")
    except RedisError:
        visits = "<i>cannot connect to Redis, counter disabled</i>"

    html = "<h3>Hello {name}!</h3>" \
           "<b>Hostname:</b> {hostname}<br/>" \
           "<b>Visits:</b> {visits}"
    return html.format(name=os.getenv("NAME", "world"), hostname=socket.gethostname(), visits=visits)

@app.route('/new', methods=["GET", "POST"])
def new_host():
    if request.method == 'POST':
        host = mdb.Host()
        host.title = request.form['title']
        host.text = request.form['text']
        host.save()
        return redirect(url_for('show_all'))
    return render_template('new.html')

@app.route('/show-all')
def show_all():
    hosts = mdb.host.find()
    return render_template('list.html', hosts=hosts)