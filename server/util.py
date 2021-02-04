from functools import wraps
from json import JSONEncoder

from faunadb.objects import Ref
from flask import abort
from flask import current_app
from flask import request


class MyEncoder(JSONEncoder):
    def default(self, o):
        if type(o) == Ref:
            return o.id()
        return o


def requires_user(func):
    """updates the app's `fauna_client` with the received token.
    Raises a `401` if the token is missing from the request headers.

    Args:
        func (function): The function to be wrapped
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        authorization_header = request.headers.get('Authorization')
        if not authorization_header:
            abort(401)
        current_app.fauna_client = current_app.fauna_client.new_session_client(
            authorization_header.split(' ', 1)[1])
        return func(*args, **kwargs)
    return wrapper
