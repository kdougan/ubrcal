from flask import jsonify
from flask import make_response
from flask import request
from flask import session
from flask import abort
from flask import Blueprint
from flask import current_app

from . import fauna
from .util import requires_user

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/current-identity', methods=['GET'])
@requires_user
def current_identity():
    return jsonify(fauna.get_current_identity())


@api.route('/login', methods=['POST'])
def login():
    data = fauna.login(request.json)
    if not data:
        abort(401)
    response = make_response(jsonify(data))
    response.set_cookie(current_app.client_cookie_name,
                        data['data']['token'],
                        max_age=60*60*8)
    return response


@api.route('/logout', methods=['POST'])
@requires_user
def logout():
    fauna.logout()
    session.pop('username', None)
    response = make_response(jsonify({'data': {'message': 'success'}}))
    response.delete_cookie(current_app.client_cookie_name)
    return response


@api.route('/account', methods=['POST'])
@requires_user
def account():
    fauna.create_account(request.json)
    data = fauna.login(request.json)
    response = make_response(jsonify(data))
    response.set_cookie(current_app.client_cookie_name,
                        data['data']['token'],
                        max_age=60*60*8)
    return response


@api.route('/user', methods=['POST'])
@requires_user
def user():
    return jsonify(fauna.create_user(request.json))
