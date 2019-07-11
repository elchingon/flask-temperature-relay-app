from threading import Lock
from flask import Flask
from .data import db
from flask_socketio import SocketIO, emit


socketio = SocketIO()
# socketio.init_app(app)
thread = None
thread_lock = Lock()

def create_app(debug=False):
  app = Flask(__name__)
  # app.debug = debug
  # app = Flask(__name__, instance_relative_config=True)
  app.config['SECRET_KEY'] = 'gjr39dkjn344_!67#'
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ac-control2.db'
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

  # app.config.from_object('config.BaseConfiguration')
  db.init_app(app)
  
  with app.app_context():
    db.create_all()
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    socketio.init_app(app,async_mode="eventlet")

  return app
