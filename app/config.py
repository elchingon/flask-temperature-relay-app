from os.path import abspath, dirname, join

_cwd = dirname(abspath(__file__))

__author__ = "alexiicarey"


class BaseConfiguration(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'tayda rocks'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + join(_cwd, 'ac-control.db')
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    HASH_ROUNDS = 100000


class TestConfiguration(BaseConfiguration):
    TESTING = True
    WTF_CSRF_ENABLED = False

    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # + join(_cwd, 'testing.db')

    # Since we want our unit tests to run quickly
    # we turn this down - the hashing is still done
    # but the time-consuming part is left out.
    HASH_ROUNDS = 1


class DebugConfiguration(BaseConfiguration):
    DEBUG = True
