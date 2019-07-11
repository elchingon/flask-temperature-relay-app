#!/usr/bin/env python
""" Open and close relay on a specific gpio pin """
import time
import sys

global SHOULD_FAKE
SHOULD_FAKE = False

try:
  import RPi.GPIO as GPIO
except ImportError:
  SHOULD_FAKE = True


RELAY_PIN = 23
STATE = False

def set_relay_pin(pin_id):
  if pin_id: 
    RELAY_PIN = pin_id

# if len(sys.argv) < 2:
#     print("Usage: relay (open|close) [gpio_pin]");
#     sys.exit();
# else:

def set_state(state):
  STATE = True if state.lower() == 'close' else False;
  print("Opening" if STATE else "Closing");

def trigger_relay(state, pin = RELAY_PIN):
  if not SHOULD_FAKE:
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM);
    GPIO.setup(pin, GPIO.OUT);
    GPIO.output(pin, state);
    time.sleep(2)
  else:
    print("SHOULDFAKE")
