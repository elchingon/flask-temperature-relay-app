from flask import session, redirect, url_for, render_template, request, current_app
from . import main

from flask import Blueprint, flash, jsonify, Response, request, render_template, redirect, url_for
from flask_socketio import emit
# from .. import socketio, thread_lock
from ..data import db
from .forms import TemperatureSensorForm
from .models import TemperatureSensor
from .. import relay
from .helper_methods import temperature_request

import json
import logging
import time

id1_max=27
id2_max=25
id3_max=25
id1_min=25
id2_min=24
id3_min=23

@main.context_processor
def provide_constants():
  return {"constants": {"APP_NAME": "Tayda Temperature Control App", "AC_CONTROL_VERSION": 3}}

@main.route("/", methods=['GET','POST'])
def index():
  # id1_temp = temperature_request('http://69.146.20.99:5000') # temperature_request('http://v2temp1.local:5555') 
  # id2_temp = temperature_request('http://69.146.20.99:5000', 2) # temperature_request('http://v2temp1.local:5555') 
  # id3_temp = temperature_request('http://69.146.20.99:5000') # temperature_request('http://v2temp1.local:5555') 
  id1_temp = temperature_request('http://v2temp1.local:5555') 
  id2_temp = temperature_request('http://v2temp2.local:5556')
  id3_temp = temperature_request('http://v2temp3.local:5557')

  temp1 = TemperatureSensor.query.filter_by(title="v2temp1").first()
  temp2 = TemperatureSensor.query.filter_by(title="v2temp2").first() 
  temp3 = TemperatureSensor.query.filter_by(title="v2temp3").first() 

  form = TemperatureSensorForm(formdata=request.form)
  
  if form.validate_on_submit():
    set_temperatures(form, 1, temp1)
    set_temperatures(form, 2, temp2)
    set_temperatures(form, 3, temp3)
    flash("Temperatures updates successfully.")
  else:
    if temp1 is not None:
      form.temp1_min_temp = temp1.min_temp
      form.temp1_max_temp = temp1.max_temp
    if temp2 is not None:
      form.temp2_min_temp = temp2.min_temp
      form.temp2_max_temp = temp2.max_temp
    if temp3 is not None:
      form.temp3_min_temp = temp3.min_temp
      form.temp3_max_temp = temp3.max_temp

  return render_template("index.html", temp_1=id1_temp, temp_2=id2_temp, temp_3=id3_temp, form=form)


def set_temperatures(form, index, temperature_record=None):
  if temperature_record == None:
    temperature_record = TemperatureSensor(title="v2temp"+str(index))
    db.session.add(temperature_record)

  min_temp = 25
  max_temp = 27.5

  if index == 1:
    min_temp = form.data.temp1_min_temp
    max_temp = form.data.temp1_min_temp
  elif index == 2:
    min_temp = form.data.temp2_min_temp
    max_temp = form.data.temp2_min_temp
  elif index == 3:
    min_temp = form.data.temp3_min_temp
    max_temp = form.data.temp3_min_temp

  temperature_record.min_temp = min_temp
  temperature_record.max_temp = max_temp

  db.session.commit()

def get_min_max(temp_id):
  # app = current_app._get_current_object()
  # with app.app_context():    
  temperature_record = TemperatureSensor.query.filter_by(title=temp_id).first()

  if temperature_record is not None:
    temp_min = temperature_record.min_temp
    temp_max = temperature_record.max_temp
  else:
    temp_min = 24.4
    temp_max = 27.4

  return temp_min, temp_max