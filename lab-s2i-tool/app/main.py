#!/usr/bin/env python

from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello(): return "Hello, World!"


@app.route("/ping")
def ping(): return "Pong"


@app.route("/healthz")
def healthz(): return "ok"

