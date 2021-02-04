import numpy as np

def find_sync(array):

	pivot = bool(array[0])
	pivot = not pivot
	pivot = int(pivot)

	indexes_M = np.where(array == pivot)
	indexes = indexes_M[0]

	if np.size(indexes) == 0:
		count = 1000
	else:
		count = indexes[0]

	

	return count



