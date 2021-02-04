import numpy as np
#import h5py

def write_acq_file(a_file, t, time, fmt):
	# Uncomment for txt
	#print('/n')
	#print('write_acq: {}'.format(t))

	np.savetxt(a_file, t, fmt=fmt, delimiter='	', newline='\n', header='', footer='', comments ='')

	# Uncomment for hdf5
	#print ('comecou')
	#a_file.create_dataset(time , data=t, chunks=True)
	#print ('0la')
