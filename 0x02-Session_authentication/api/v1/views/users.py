#!/usr/bin/env python3
''' users view module'''
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def view_all_users() -> str:
    ''' display all list of users using get method'''
    all_users = [user.to_json() for user in User.all()]
    return jsonify(all_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def view_one_user(user_id: str = None) -> str:
    ''' display a user by inserting the user_id'''
    if user_id is None:
        abort(404)
    if user_id == 'me':
        if request.current_user is None:
            abort(404)
        return jsonify(request.current_user.to_json()), 200
    user = User.get(user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_json())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id: str = None) -> str:
    ''' delete a user account'''
    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)
        user.remove()
        return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user() -> str:
    ''' create a new user'''
    entry = None
    err_msg = None
    try:
        entry = request.get_json()
    except Exception as e:
        entry = None
    if entry is None:
        err_msg = "Wrong format"
    if err_msg is None and entry.get('email', "") == "":
        err_msg = "email missing"
    if err_msg is None and entry.get('password', "") == "":
        err_msg = "password missing"
    if err_msg is None:
        try:
            user = User()
            user.email = entry.get("email")
            user.password = entry.get("password")
            user.first_name = entry.get("first_name")
            user.last_name = entry.get("last_name")
            user.save()
            return jsonify(user.to_json()), 201
        except Exception as e:
            err_msg = "Can't create User: {}".format(e)
    return jsonify({'error': err_msg}), 400


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id: str = None) -> str:
    ''' update user profile'''
    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)
    entry = None
    try:
        entry = request.get_json()
    except Exception as e:
        entry = None
    if entry is None:
        return jsonify({'error': "Wrong format"}), 400
    if entry.get('first_name') is not None:
        user.first_name = entry.get('first_name')
    if entry.get('last_name') is not None:
        user.last_name = entry.get('last_name')
    user.save()
    return jsonify(user.to_json), 200
