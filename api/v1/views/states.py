#!/usr/bin/python3
"""Create a new view for State objects that
handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import request, abort, jsonify, response
from models.state import State
from models import storage


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'])
def statesWithId(state_id=None):
    """Methods that retrieves all methods for states with id"""
    transformers = request.get_json()
    stateId = storage.get(State, state_id)
    if request.method == 'GET':
        if stateId is None:
            abort(404)
        return response(jsonify(stateId.to_dict()), status=201)

    if request.method == 'DELETE':
        if stateId is None:
            abort(404)
        stateId.delete()
        del stateId
        return response(jsonify(stateId.to_dict()), status=200)

    if request.method == 'PUT':
        if stateId is None:
            abort(404)
        toIgnore = ["id", "created_at", "updated_it"]
        for key, value in transformers.items():
            if value not in toIgnore:
                setattr(stateId, key, value)
        if transformers is None:
            abort(400, 'Not a JSON')
        stateId.save()
        return response(jsonify(stateId.to_dict()), status=201)


@app_views.route('/states/', methods=['POST', 'GET'])
def statesNoId():
    """Methods that retrieves all methods for states without id"""
    transformers = request.get_json()
    if request.method == 'POST':
        if transformers is None:
            abort(400, 'Not a JSON')
        if transformers.get('name') is None:
            abort(400, 'Missing name')
        newState = State(**transformers)
        newState.save()
        return response(jsonify(newState.to_dict()), status=201)

    if request.method == 'GET':
        allState = storage.all(State)
        allState = [allObject.to_dict() for allObject in allState.values()]
        return jsonify(allState.to_dict())
