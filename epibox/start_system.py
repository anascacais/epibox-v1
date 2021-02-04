from sync_bitalino import * 
from write_file import * 
import time
from read_modules import * 
from sync_drift import * 
from bitalino import *
from system_except import * 
import sys
import numpy as np
from datetime import datetime, timedelta




def start_system(devices, a_file, drift_log_file, fs, mac_channels, sensors, save_fmt, resolution):

    dig_Out = 0
    now = datetime.now()
    sync_param = {'flag_sync' : 0 , 'inittime' : time.time(), 'strtime': time.time(), 'sync_time' : now.strftime("%Y-%m-%d %H:%M:%S.%f").rstrip('0'), 'dig_Out' : dig_Out, 'close_file' : 0, 'diff': 1000, 'save_log': 1, 'count_a': 1000, 'sync_append': 0}
    
    for i in range(len(devices)):
        sync_param['sync_arr_'+chr(ord('@')+i+1)] = np.zeros(1000, dtype = float)
        
    
    sync_param['dig_Out'] = sync_bitalino(dig_Out, devices[0])
        
    # Initialize devices
    for device in devices:
        channels = [int(elem[1])-1 for elem in mac_channels if elem[0]==device.macAddress]
        device.start(SamplingRate=fs, analogChannels=channels)
        print('START SYSTEM')
    
    try:
        #Default to 0
        sync_param['dig_Out'] = sync_bitalino(sync_param['dig_Out'], devices[0])
    
    except Exception as e:
        print(e)
        pass
    
    now = datetime.now()
    print('start {}'.format(datetime.now()))
    sync_param['sync_time'] = now.strftime("%Y-%m-%d %H:%M:%S.%f")
    print(now.strftime("%Y-%m-%d %H:%M:%S.%f"))
    t, t_str, t_display = read_modules(devices, mac_channels, sensors, resolution)
    
    
    #sync_param['diff'], sync_param['count_a'] = sync_drift(t)
    sync_param['save_log'] = 1
			
    write_file(t, a_file, drift_log_file, sync_param, str(sync_param['inittime']), save_fmt)
    print('System initiated')                    
    
    return t, t_display, sync_param
	
