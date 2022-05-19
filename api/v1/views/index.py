#!/usr/bin/python
from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status')
def status():
    stat = {"status": "OK"}
    return jsonify(stat)
