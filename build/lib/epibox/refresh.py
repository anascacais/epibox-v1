def refresh(data, data_socket):
	


	for i in range(0,12):

		if i < 7 :
			data[:-100,i] = data[100:,i]

			data[-100:,i] = data_socket[:,5+i].ravel()
		else : 
			data[:-100,i] = data[100:,i]

			data[-100:,i] = data_socket[:,10+i].ravel()



	data[:-100,12] = data[100:,12]
	data[-100:,12] = data_socket[:,4].ravel()

	data[:-100,13] = data[100:,13]
	data[-100:,13] = data_socket[:,12].ravel()

	return data 	



