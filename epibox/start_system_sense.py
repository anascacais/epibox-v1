import time
from datetime import datetime, timedelta


def start_system():

    dig_Out = 0
    now = datetime.now()
    sync_param = {'flag_sync' : 0 , 'inittime' : time.time(), 'strtime': time.time(), 'sync_time' : now.strftime("%Y-%m-%d %H:%M:%S.%f").rstrip('0'), 'dig_Out' : dig_Out, 'close_file' : 0, 'diff': 1000, 'save_log': 1, 'count_a': 1000, 'sync_append': 0}
    sync_param['save_log'] = 1
            
    print('System initiated')                    
    
    return sync_param