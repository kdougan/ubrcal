import requests

from faunadb.client import FaunaClient
from flask import Flask
from flask import abort
from flask import request
from flask.json import jsonify
from flask.templating import render_template
from flask_cors import CORS

from . import fauna
from .api_routes import api
from .util import MyEncoder
from .util import requires_user

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
app.json_encoder = MyEncoder

app.secret_key = 'd40b8895-116a-4d43-b2e4-3cded449980c'
app.server_key = 'fnAEAx4lITACCI3Q4il2ADKgeTyo1n7jm92-wRAH'
app.session_cookie_name = 'ubrcal session'
app.client_cookie_name = 'ubrcal token'

app.fauna_graphql_endpoint = 'https://graphql.fauna.com/graphql'
app.server_fauna_client = FaunaClient(secret=app.server_key)


@app.before_request
def before_request():
    app.fauna_client = app.server_fauna_client


app.register_blueprint(api)


@app.route('/')
def index():
    return render_template('index.html')


@requires_user
@app.route('/graphql', methods=['POST'])
def graphql():
    return jsonify(fauna.query_graphql(request))
