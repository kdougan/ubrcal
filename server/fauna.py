import requests

from dateutil import parser
from faunadb import query as q
from flask import abort
from flask import current_app
from hashlib import md5


def query_graphql(request):
    authorization_header = request.headers.get('Authorization')
    if not authorization_header:
        abort(401)
    response = requests.post(
        current_app.fauna_graphql_endpoint,
        headers={'Authorization': authorization_header},
        json=request.json
    )
    return response.json()


def get_current_identity():
    try:
        return current_app.fauna_client.query(
            q.get(q.current_identity())
        )
    except Exception as e:
        print(e)


def login(data):
    try:
        return current_app.fauna_client.query(
            q.let(
                {
                    'response': q.login(
                        q.match(q.index('unique_account_username_type'),
                                [data.get('username'), 'EMAIL']),
                        {'password': data.get('password')}
                    ),
                    'user': q.select_with_default(
                        ['data', 'user'],
                        q.get(
                            q.select(['instance'], q.var('response'))),
                        None
                    )
                },
                {
                    'data': {
                        'token': q.select('secret', q.var('response')),
                        'user': q.if_(
                            q.is_ref(q.var('user')),
                            q.select(['data', 'alias'],
                                     q.get(q.var('user'))),
                            None
                        )
                    }
                }
            )
        )
    except Exception as e:
        print(e)


def logout():
    try:
        return current_app.fauna_client.query(
            q.logout(True)
        )
    except Exception as e:
        print(e)


def create_account(data):
    try:
        return current_app.fauna_client.query(
            q.create(
                q.collection('accounts'),
                {
                    'credentials': {
                        'password': data.get('password'),
                    },
                    'data': {
                        'username': data.get('username'),
                        'type': 'EMAIL'
                    }
                }
            )
        )
    except Exception as e:
        if 'not unique' in str(e):
            abort(
                409, f'Account with email {data.get("username")} already exists')
        print(e)


def create_user(data):
    try:
        current_identity = get_current_identity()
        email_hash = md5(
            current_identity['data']['username'].encode('utf-8')).hexdigest()
        return current_app.fauna_client.query(
            q.if_(
                q.is_ref(q.select_with_default(
                    ['data', 'user'],
                    q.get(q.current_identity()),
                    None
                )),
                q.abort('exists'),
                q.let(
                    {
                        'userMetaRef': q.new_id(),
                        'userRef': q.new_id()
                    },
                    q.do(
                        q.create(
                            q.ref(q.collection('user_metas'),
                                  q.var('userMetaRef')),
                            {
                                'data': {
                                    'name': data.get('name'),
                                    'email': q.select(
                                        ['data', 'username'],
                                        q.get(q.current_identity())
                                    ),
                                    'dob': parser.parse(data.get('dob')).date()
                                }
                            }
                        ),
                        q.create(
                            q.ref(q.collection('users'),
                                  q.var('userRef')),
                            {
                                'data': {
                                    'alias': data.get('alias'),
                                    'avatar': f'https://www.gravatar.com/avatar/{email_hash}',
                                    'public': False,
                                    'meta': q.ref(
                                        q.collection('user_metas'),
                                        q.var('userMetaRef')
                                    ),
                                }
                            }
                        ),
                        q.update(
                            q.current_identity(),
                            {
                                'data': {
                                    'user': q.ref(
                                        q.collection('users'),
                                        q.var('userRef')
                                    )
                                }
                            }
                        ),
                        q.call('current_user', [])
                    )
                )
            )
        )
    except Exception as e:
        if str(e) == 'exists':
            abort(409, 'User for current identity already exists.')
        print(e)
