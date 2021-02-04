def sync_drift(t, count_a, count_b)
	a_I1 = t[0:,2]
	b_I1 = t[0:,12]
	count_a_t = find_sync(a_I1)
	count_b_t = find_sync(b_I1)

	if count_a_t == 1000 or count_b_t == 1000:
		flag_sync = 1
		count_a = count_a + count_a_t
		count_b = count_b + count_b_t
	else:
		flag_sync = 0
		count_a = count_a + count_a_t
		count_b = count_b + count_b_t
		diff = count_a - count_b

	return diff
	