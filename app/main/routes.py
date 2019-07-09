from flask import session, redirect, url_for, render_template, request
from . import main

from flask import Blueprint, flash, jsonify, Response, request, render_template, redirect, url_for
from flask_socketio import emit
# from .. import socketio, thread_lock
from ..data import db
from .forms import TemperatureSensorForm
from .models import TemperatureSensor
from .. import relay

import json
import logging
import time

@main.context_processor
def provide_constants():
  return {"constants": {"APP_NAME": "Tayda Temperature Control App", "AC_CONTROL_VERSION": 3}}

@main.route("/", methods=['GET','POST'])
def index():
  id1_temp = "26" #temperature_request('http://raspberrypi.local:5000') #temperature_request('http://v2temp1.local:5555')
  id2_temp = "27.5" #temperature_request('http://raspberrypi.local:5000', 2) #temperature_request('http://v2temp2.local:5556')
  id3_temp = "27" #temperature_request('http://v2temp3.local:5557')

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
    if temp1 != None:
      form.temp1_min_temp = temp1.min_temp
      form.temp1_max_temp = temp1.max_temp
    if temp2 != None:
      form.temp2_min_temp = temp2.min_temp
      form.temp2_max_temp = temp2.max_temp
    if temp3 != None:
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

