from write_drift_log import *
from write_acq_file import *

def write_file(t, a_file, drift_log_file, sync_param, time, fmt):
#     if sync_param['save_log'] == 1:
#         write_drift_log(drift_log_file, sync_param)
#         sync_param['save_log'] = 0
    
    write_acq_file(a_file, t, time, fmt)
    # line added to see if it fixes drift_log_file
    write_drift_log(drift_log_file, sync_param)
    print('save_log: {}'.format(sync_param['save_log']))
    
