from close_file import * 
from bitalino import * 


def disconnect_system(devices, a_file, annot_file, drift_log_file): 

    for i,device in enumerate(devices):
        try:
            device.stop()
            device.close()
        except:
            continue

    close_file(a_file, annot_file, drift_log_file)
