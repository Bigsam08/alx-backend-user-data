#!/usr/bin/env python3
''' user authentication module'''
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> str:
    ''' main entry program for users to login'''
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None or email == '':
        return jsonify({'error': "email missing"}), 400
    if password is None or password == "":
        return jsonify({'error': "password missing"}), 400
    user = User.search({'email': email})
    if len(user) == 0:
        return jsonify({'error': "no user found for this email"}), 400
    user = user[0]
    if not user.is_valid_password(password):
        return jsonify({'error': "wrong password"}), 401
    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    cookie_name = getenv('SESSION_NAME')
    response = jsonify(user.to_json())
    response.set_cookie(cookie_name, session_id)
    return response


@app_views.route('/auth_session/logout',
                 methods=['DELETE'],
                 strict_slashes=False)
def logout() -> str:
    ''' delete session and log user out'''
    from api.v1.app import auth
    if auth.destroy_session(request) is False:
        abort(404)
    return jsonify({}), 200
