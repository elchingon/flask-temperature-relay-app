from flask import session, copy_current_request_context
from flask_socketio import emit, disconnect
from .. import socketio, thread_lock, thread
from .. import relay
from .models import TemperatureSensor
from .helper_methods import temperature_request, get_relay_pin

import requests
import json
import logging
import time


@socketio.on('connect', namespace='/ac_control')
def ac_control_connect():
  global thread
  with thread_lock:
    if thread is None:
      logging.info("Starting Thread")
      thread = socketio.start_background_task(run_ac_control)
      emit('connect', {'data': 'Connected'}, namespace='/ac_control')

@socketio.on('rerun_ac_control', namespace='/ac_control')
def rerun_ac_control(id1_min, id1_max, id2_min, id2_max, id3_min, id3_max):
  run_ac_control(id1_min, id1_max, id2_min, id2_max, id3_min, id3_max)
  # emit('temp_response', { 'new_temp': str(new_temp), 'temp_id': temp_id }, namespace='/ac_control')

@socketio.on('turn_on_relay_event', namespace='/ac_control')
def turn_on_relay_event(temp_id):
  turn_on_relay(temp_id)

@socketio.on('turn_off_relay_event', namespace='/ac_control')
def turn_off_relay_event(temp_id):
  turn_off_relay(temp_id)

@socketio.on('disconnect_request', namespace='/test')
def disconnect_request():
    @copy_current_request_context
    def can_disconnect():
        disconnect()

    session['receive_count'] = session.get('receive_count', 0) + 1
    # for this emit we use a callback function
    # when the callback function is invoked we know that the message has been
    # received and it is safe to disconnect
    emit('temp_response',
         {'data': 'Disconnected!', 'count': session['receive_count']},
         callback=can_disconnect)

      
def run_ac_control(id1_min=25, id1_max=27, id2_min=24, id2_max=25, id3_min=23, id3_max=25):  
  try:
    # id1_temp = temperature_request('http://69.146.20.99:5000') # temperature_request('http://v2temp1.local:5555') 
    # id2_temp = temperature_request('http://69.146.20.99:5000', 2) # temperature_request('http://v2temp1.local:5555') 
    id1_temp = temperature_request('http://v2temp1.local:5555') 
    socketio.emit('temp_response', { 'data': id1_temp, 'temp_id': 'temp_1' }, namespace='/ac_control')
    id2_temp = temperature_request('http://v2temp2.local:5556')
    socketio.emit('temp_response', { 'data': id2_temp, 'temp_id': 'temp_2' }, namespace='/ac_control')
    id3_temp = temperature_request('http://v2temp3.local:5557')
    socketio.emit('temp_response', { 'data': id3_temp, 'temp_id': 'temp_3' }, namespace='/ac_control')
    
    #Turn on Blowers - should be on all the time
    relay.trigger_relay(False, 17)
    relay.trigger_relay(False, 27)
    relay.trigger_relay(False, 22)
     
    if float(id1_temp) >= float(id1_max) and float(id2_temp) >= float(id2_max) and float(id3_temp) >= float(id3_max):
      logging.info("Compressors on")
      turn_on_relay('temp_1')
      turn_on_relay('temp_2')
      turn_on_relay('temp_3')
    elif float(id1_temp) <= float(id1_min) and float(id2_temp) <= float(id2_min) and float(id3_temp) <= float(id3_min):
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
  except Exception as e:
    print(e)
    logging.warning("Quit" )
      
def turn_off_relay(temp_id):
  relay_pin = get_relay_pin(temp_id)
  relay.trigger_relay(True, relay_pin)
  print("Relay off for " + temp_id + " Pin " + str(relay_pin))
  socketio.emit('compressor_response', {'data': 'Off', 'temp_id': temp_id}, namespace='/ac_control')

def turn_on_relay(temp_id):
  relay_pin = get_relay_pin(temp_id)
  relay.trigger_relay(False, relay_pin)
  print("RElay on for " + temp_id + " Pin " + str(relay_pin))
  socketio.emit('compressor_response', {'data': 'On', 'temp_id': temp_id}, namespace='/ac_control')
