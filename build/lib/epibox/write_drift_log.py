import numpy as np

def write_drift_log(filename, sync_param):
    drift = sync_param['diff']
    sync_time = sync_param['sync_time']
    count_a = sync_param['count_a']

#     filename.write('%i' % count_a)
#     filename.write('%s' % ' ')
#     filename.write('%i' % drift)
#     filename.write('%s' % '  ' + sync_time + '\n')

    if not sync_param['mode']:
        filename.write('%s' % sync_time + '\n')
        sync_param['mode'] = 1
    else:
        filename.write('\n')
    
    print('%s' % '  ' + sync_time)