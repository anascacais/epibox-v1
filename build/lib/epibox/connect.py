import sys
from bitalino import *
import time
import ast
import string
import random
import paho.mqtt.client as mqtt
import ast
import json


def connect(macAddress, init_time, client_name):

    print('Searching for Module...' + macAddress)
    
    host_name = '192.168.0.10'
    topic = 'rpi'
    client = mqtt.Client('cenas')
    client.publish('rpi', "['test']")
    print('test')
    
    while True:

        if (time.time() - init_time) > 60:
            sys.exit('Timeout for connection! Exiting python. ')
        try:

            device = BITalino(macAddress, timeout=5)

            # Read BITalino version
            #print(device.version())
            print('Device {} connected!'.format(macAddress))

            return device

        except Exception as e:
            print(e)
            print('HERE')
            time.sleep(10)
            timeout_json = json.dumps(['TIMEOUT', macAddress])
            client.publish('rpi', timeout_json)




