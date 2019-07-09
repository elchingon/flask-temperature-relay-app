flask-socketio-temperature-relay-app
===================

An application to read output on flask for DS18B20 OneWire temperature sensor and trigger relay pins. 
Uses Flask-SQLAlchemy, Flask-WTF and Flask-SocketIO application.

To run this application install the requirements in a virtual environment

    $ pip install -r requirements.txt

    $ python ./db_creator.py


Then run `python run.py` and visit `http://localhost:5000` on one or more browser tabs.

    $ python run.py


Socketio implementation inspired by Miguel Grinberg's [@miguelgrinberg](https://github.com/miguelgrinberg) [Flask-SocketIO-Chat App](https://github.com/miguelgrinberg/Flask-SocketIO-Chat)
