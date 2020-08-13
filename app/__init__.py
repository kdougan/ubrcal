#coding: utf-8

from flask import jsonify
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_graphql import GraphQLView
from flask_graphql_auth import GraphQLAuth


from config import Config

db = SQLAlchemy()


def create_app():

    app = Flask(__name__)

    app.config.from_object(get_environment_config())

    db.init_app(app)
    migrate = Migrate(app, db)
    auth = GraphQLAuth(app)

    from app.schema import schema
    app.add_url_rule(
        '/graphql',
        view_func=GraphQLView.as_view(
            'graphql',
            schema=schema,
            graphiql=True
        )
    )

    @app.before_first_request
    def initialize_database():
        ''' Create all tables '''
        db.create_all()

    @app.route('/')
    def hello_world():
        return 'Hello World'

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    return app


def get_environment_config():
    if Config.ENV == 'PRODUCTION':
        return 'config.ProductionConfig'
    elif Config.ENV == 'DEVELOPMENT':
        return 'config.DevelopmentConfig'
