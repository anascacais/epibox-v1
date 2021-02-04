import re
import numpy as np

def find(s, ch):
	arr = np.zeros(1000)
	i = 0
	return [pos for pos, char in enumerate(s) if char == ch]
