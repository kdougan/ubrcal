# ./config.py
import os

from dotenv import load_dotenv

load_dotenv()


class Config(object):
    ENV = os.getenv('ENV')
    CSRF_ENABLED = True
    SECRET_KEY = os.getenv('SECRET_KEY')
    # Database Configuration
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('SECRET_KEY')
    REFRESH_EXP_LENGTH = os.getenv('REFRESH_EXP_LENGTH', 30)
    ACCESS_EXP_LENGTH = os.getenv('ACCESS_EXP_LENGTH', 30)


class DevelopmentConfig(Config):
    DEBUG = True
    DB_USERNAME = os.getenv('DB_USERNAME')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_DATABASE = os.getenv('DB_DATABASE')
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:3306/{DB_DATABASE}'


class ProductionConfig(Config):
    DEBUG = False
    DB_USERNAME = os.getenv('DB_USERNAME')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_DATABASE = os.getenv('DB_DATABASE')
    CLEARDB_DATABASE_URL = os.getenv('CLEARDB_DATABASE_URL')
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:3306/{DB_DATABASE}'
    if CLEARDB_DATABASE_URL:
        SQLALCHEMY_DATABASE_URI = CLEARDB_DATABASE_URL.replace(
            'mysql', 'mysql+pymysql')
        if '?' in SQLALCHEMY_DATABASE_URI:
            SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.split('?')[0]
