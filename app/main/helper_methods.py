import requests
import logging
import time
import json

def get_min_max_defaults(temp_id):
  # id1_min=25, id1_max=27, id2_min=24, id2_max=25, id3_min=23, id3_max=25
  switcher = {
    "temp_1": [25,27], 
    "temp_2": [24, 25],
    "temp_3": [23, 25]
  }
  # print(switcher.get(temp_id, 0))
  return switcher.get(temp_id, 0)    

def get_relay_pin(temp_id):
  switcher = {
    "temp_1": 23,
    "temp_2": 24,
    "temp_3": 25
  }
  # print(switcher.get(temp_id, 0))
  return switcher.get(temp_id, 0) 

def temperature_request(api_url, index = 1): 
  request_pending = False
  num_requests = 0 
  total_requests = 4
  while request_pending is False and num_requests < total_requests: 
    try:
      num_requests += 1
      query_url = api_url
      r = requests.get(query_url)
      if r.status_code != 200:
        print("Error:", r.status_code)
          
      json_resp = r.json()
      request_pending= True
      print(json_resp)
      id_temp = float(json_resp['temp_' + str(index)])
      return id_temp  
    except requests.exceptions.HTTPError as errh:
      num_requests += 1
      logging.warning("Http Error:" + errh)
      if (num_requests < total_requests):
        time.sleep(5)
        continue
    except requests.exceptions.Timeout as errt:
      num_requests += 1
      logging.warning("Timeout Error:" + errt)     
      if (num_requests < total_requests):
        time.sleep(5)
        continue
    except requests.exceptions.ConnectionError as errc:
      num_requests += 1
      logging.warning("Error Connecting:" + str(errc))
      if (num_requests < total_requests):
        time.sleep(5)
        continue
    except requests.exceptions.RequestException as err:
      num_requests += 1
      logging.warning("OOps: Something Else" + err)
      if (num_requests < total_requests):
        time.sleep(5)
        continue
    except Exception as e:
      num_requests += 1
      print(e)
      if (num_requests < total_requests):
        logging.warning("Quit" )
        continue  

   
      