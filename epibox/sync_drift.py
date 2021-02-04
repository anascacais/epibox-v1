from bitalino import *
from find_sync import *
from system_except import * 

def sync_drift(a_I1, b_I1):
    count_a_t = find_sync(a_I1)
    count_b_t = find_sync(b_I1)

    if count_a_t == 1000 or count_b_t == 1000:
        count_a = 0
        count_b = 0
        #raise ConnectionBad
    else:
        count_a = count_a_t
        count_b = count_b_t

    diff = count_b - count_a

    return diff, count_a
	
