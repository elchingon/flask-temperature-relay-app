from flask import session
from flask_socketio import emit
from .. import socketio, thread_lock, thread
from .. import relay

import requests
import json
import logging
import time


id1_max=25
id2_max=25
id3_max=25
id1_min=24
id2_min=24
id3_min=24


@socketio.on('connect', namespace='/ac_control')
def ac_control_connect():
  global thread
  with thread_lock:
    if thread is None:
      logging.info("Starting Thread")
      thread = socketio.start_background_task(run_ac_control)
      set_min_max_values()  
      emit('connect', {'data': 'Connected'}, namespace='/ac_control')

@socketio.on('rerun_ac_control', namespace='/ac_control')
def rerun_ac_control():
  run_ac_control()
  # emit('temp_response', { 'new_temp': str(new_temp), 'temp_id': temp_id }, namespace='/ac_control')

@socketio.on('turn_on_relay_event', namespace='/ac_control')
def turn_on_relay_event(temp_id):
  turn_on_relay(temp_id)

@socketio.on('turn_off_relay_event', namespace='/ac_control')
def turn_off_relay_event(temp_id):
  turn_off_relay(temp_id)

def set_min_max():
  temp1 = TemperatureSensor.query.filter_by(title="v2temp1").first()
  temp2 = TemperatureSensor.query.filter_by(title="v2temp2").first() 
  temp3 = TemperatureSensor.query.filter_by(title="v2temp3").first()

  if temp1 != None:
      id1_min = temp1.min_temp
      id1_max = temp1.max_temp
  if temp2 != None:
      id2_min = temp2.min_temp
      id2_max = temp2.max_temp
  if temp3 != None:
      id3_min = temp3.min_temp
      id3_max = temp3.max_temp
      
def run_ac_control():  
  try:
    id1_temp = temperature_request('http://raspberrypi.local:5000') # temperature_request('http://v2temp1.local:5555') 
    # id1_temp = temperature_request('http://v2temp1.local:5555') 
    socketio.emit('temp_response', { 'data': id1_temp, 'temp_id': 'temp_1' }, namespace='/ac_control')
    id2_temp = temperature_request('http://raspberrypi.local:5000', 2) # temperature_request('http://v2temp1.local:5555') 
    # id2_temp = temperature_request('http://v2temp2.local:5556')
    socketio.emit('temp_response', { 'data': id2_temp, 'temp_id': 'temp_2' }, namespace='/ac_control')
    id3_temp = 27 #temperature_request('http://v2temp3.local:5557')
    socketio.emit('temp_response', { 'data': id3_temp, 'temp_id': 'temp_3' }, namespace='/ac_control')
    
    #Turn on Blowers - should be on all the time
    relay.trigger_relay(False, 17)
    relay.trigger_relay(False, 27)
    relay.trigger_relay(False, 22)
    
    if id1_temp >= id1_max and id2_temp >= id2_max and id3_temp >= id3_max:
      logging.info("Compressors on")
      turn_on_relay('temp_1')
      turn_on_relay('temp_2')
      turn_on_relay('temp_3')
    elif id1_temp <= id1_min and id2_temp <= id2_min and id3_temp <= id3_min:
      logging.info("Compressors off")
      turn_off_relay('temp_1')
      turn_off_relay('temp_2')
      turn_off_relay('temp_3')
    
    logging.info("Temp1:"+str(id1_temp))
    logging.info("Temp2:"+str(id2_temp))
    logging.info("Temp3:"+str(id3_temp))
    
    time.sleep(5)
  # except requests.exceptions.HTTPError as errh:
  #   logging.warning("Http Error:" + errh)
  #   time.sleep(5)
  #   continue
  # except requests.exceptions.ConnectionError as errc:
  #   logging.warning("Error Connecting:" + errc)
  #   time.sleep(5)
  #   continue
  # except requests.exceptions.Timeout as errt:
  #   logging.warning("Timeout Error:" + errt)     
  #   time.sleep(5)
  #   continue
  # except requests.exceptions.RequestException as err:
  #   logging.warning("OOps: Something Else" + err)
  #   time.sleep(5)
  #   continue
  # except KeyboardInterrupt:
  #   logging.warning("Quit")
  except:
    logging.warning("Quit")
      

def temperature_request(api_url, index = 1):  
  query_url = api_url
  r = requests.get(query_url)
  if r.status_code != 200:
    print("Error:", r.status_code)
      
  json_resp = r.json()
  print(json_resp)
  id_temp = float(json_resp['temp_' + str(index)])
  return id_temp  

def turn_off_relay(temp_id):
  relay_pin = get_relay_pin(temp_id)
  relay.trigger_relay(True, relay)
  socketio.emit('compressor_response', {'data': 'Off', 'temp_id': temp_id}, namespace='/ac_control')

def turn_on_relay(temp_id):
  relay_pin = get_relay_pin(temp_id)
  relay.trigger_relay(False, relay)
  socketio.emit('compressor_response', {'data': 'On', 'temp_id': temp_id}, namespace='/ac_control')

def get_relay_pin(temp_id):
  relay_pin = None;
  switch(temp_id):
    case 'temp_1':
      relay_pin = 23
      break
    case 'temp_2':
      relay_pin = 24
      break
    case 'temp_3':
      relay_pin = 25
      break
  return relay_pin    
      
