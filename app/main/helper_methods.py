import requests
import json

def temperature_request(api_url, index = 1):  
  query_url = api_url
  r = requests.get(query_url)
  if r.status_code != 200:
    print("Error:", r.status_code)
      
  json_resp = r.json()
  print(json_resp)
  id_temp = float(json_resp['temp_' + str(index)])
  return id_temp  

def get_relay_pin(temp_id):
  switcher = {
    "temp_1": 23,
    "temp_2": 24,
    "temp_3": 25
  }
  # print(switcher.get(temp_id, 0))
  return switcher.get(temp_id, 0)    
      