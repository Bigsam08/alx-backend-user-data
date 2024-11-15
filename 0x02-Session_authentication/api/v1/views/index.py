#!/usr/bin/env python3
''' index views module'''
from api.v1.views import app_views
from flask import abort, jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    ''' get api status and return it'''
    return jsonify({"status": "OK"})


@app_views.route('/unauthorized', methods=['GET'], strict_slashes=False)
def unauthorized() -> str:
    '''return an abort 401 for unauthorized access '''
    abort(401)


@app_views.route('/forbidden', methods=['GET'], strict_slashes=False)
def forbidden() -> str:
    '''return an abort 403 for forbidden access '''
    abort(403)


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats() -> str:
    '''return number of each object '''
    from models.user import User
    stats = {}
    stats['users'] = User.count()
    return jsonify(stats)
