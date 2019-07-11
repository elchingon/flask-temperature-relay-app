#!/bin/env python
from app import create_app, socketio
from app.db_setup import init_db

app = create_app(debug=False)
init_db()


if __name__ == '__main__':
    socketio.run(app, port=5001)
