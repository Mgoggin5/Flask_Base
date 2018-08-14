from flask import render_template, flash, redirect, url_for, request, \
    g, jsonify
from redis import Redis, RedisError
import os
import socket
from app import redis, app, mdb
from app.models import Host
from flask_mongoengine.wtf import model_form

HostForm = model_form(Host)

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
def new_host(request):
    form = HostForm(request.POST)
    if request.method == 'POST':
        redirect('Done')
    return render_template('new.htm', form = form)

@app.route('/show-all')
def show_all():
    hosts = mdb.host.find()
    return render_template('list.html', hosts=hosts)