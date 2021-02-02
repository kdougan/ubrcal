from faunadb import query as q
from faunadb.client import FaunaClient
from faunadb.objects import Ref
from flask import Flask
from flask import abort
from flask import redirect
from flask import request
from flask import session
from flask import url_for
from flask.json import jsonify
from flask.templating import render_template
from flask_cors import CORS
from typing_extensions import TypeAlias


app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
app.secret_key = 'd40b8895-116a-4d43-b2e4-3cded449980c'
app.server_key = 'fnAEAx4lITACCI3Q4il2ADKgeTyo1n7jm92-wRAH'

client = FaunaClient(secret=app.server_key)


# -----=====-----


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/login', methods=['POST'])
def login():
    data = authenticate(request.form)
    if not data:
        abort(403)
    return jsonify(data)


@app.route('/api/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/api/user', methods=['POST'])
def post_user():
    return jsonify(createUser(request.form))


# -----=====-----


def authenticate(form):
    try:
        print(form)
        return client.query(
            q.let(
                {
                    'response': q.login(
                        q.match(q.index('unique_Account_username_type'),
                                [form.get('username'), 'EMAIL']),
                        {'password': form.get('password')}
                    ),
                    'user': q.select(
                        ['data', 'user'],
                        q.get(q.select(['instance'], q.var('response')))
                    )
                },
                {
                    'data': {
                        'token': q.select('secret', q.var('response')),
                        'user': q.if_(
                            q.is_ref(q.var('user')),
                            q.select(['data', 'alias'], q.get(q.var('user'))),
                            None
                        )
                    }
                }
            )
        )
    except Exception as e:
        print(e)
    return None


def createUser(form):
    try:
        print(form)
        token = request.headers.get('ubrcalClientToken')
        if not token:
            abort(403)
        new_client = client.new_session_client(token)
        return new_client.query(
            q.let(
                {
                    'userMetaRef': q.create(
                        q.collection('user_meta'), {
                            'data': {
                                'name': form.get('name'),
                                'email': q.select(['data', 'username'], q.current_identity()),
                                'dob': form.get('dob')
                            }
                        }
                    ),
                    'userRef': q.create(
                        q.collection('users'), {
                            'data': {
                                'alias': form.get('alias'),
                                'public': False,
                                'meta': q.var('userMetaRef')
                            }
                        }
                    )
                },
                q.update(q.current_identity(), {'user': q.var('userRef')})
            )
        )
    except Exception as e:
        print(e)
    return None
