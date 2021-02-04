from connect import *
from open_file import *
import time


def connect_system(directory, devices_MAC, mac_channels, sensors, fs, client):
    
    devices = []
    
    for i, mac in enumerate(devices_MAC):
        
        init_connect_time = time.time()
        devices.append(connect(mac, init_connect_time, client))
        
    a_file, annot_file, drift_log_file = open_file(directory, devices, mac_channels, sensors, fs)
    
    return devices, a_file, annot_file, drift_log_file
