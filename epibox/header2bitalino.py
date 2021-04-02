

def header2bitalino(filename, file_time, file_date, devices, mac_channels, sensors, fs, saveRaw):
    
    filename.write('# OpenSignals Text File Format' + '\n')
    
    mac_dict = {}
    resolution = {}
    fmt = []# get format to save values in txt
    
    for n_device,device in enumerate(devices):
        
        fmt += ['%i']
        mac_dict[device.macAddress] = {}
        
        mac_dict[device.macAddress]['sensor'] = []
        for i,elem in enumerate(mac_channels):
            if elem[0]==device.macAddress:
                mac_dict[device.macAddress]['sensor'] += [sensors[i]]
                if saveRaw:
                    fmt += ['%i']
                else:
                    fmt += ['%.2f']
                
#                 if sensors[i] in ['PPG','SpO2', 'ACC', '-']:
#                     mac_dict[device.macAddress]['sensor'] += ['RAW']
#                     fmt += ['%i']
#                 else:
#                     mac_dict[device.macAddress]['sensor'] += [sensors[i]]
#                     fmt += ['%.2f']
        
        mac_dict[device.macAddress]['device name'] = 'Device '+str(n_device+1) 
        
        aux = ['A'+elem[1] for elem in mac_channels if elem[0]==device.macAddress]
        mac_dict[device.macAddress]['column'] = ["nSeq"]+aux
        
        mac_dict[device.macAddress]['sync interval'] = 2 #???
        
        mac_dict[device.macAddress]['time'] = file_time
        
        mac_dict[device.macAddress]['comments'] = ''
        
        mac_dict[device.macAddress]['device connection'] = device.macAddress
                
        mac_dict[device.macAddress]['channels'] = [int(elem[1]) for elem in mac_channels if elem[0]==device.macAddress]
        
        mac_dict[device.macAddress]['date'] = file_date
        
        mac_dict[device.macAddress]['mode'] = 0 #???
        
        mac_dict[device.macAddress]['digital IO'] = [0, 0, 0, 0, 1, 1, 1, 1] #???
        
        mac_dict[device.macAddress]['firmware version'] = device.version() 
        
        mac_dict[device.macAddress]['device'] = 'bitalino_rev'
        
        mac_dict[device.macAddress]['position'] = 0
        
        mac_dict[device.macAddress]['sampling rate'] = fs
        
        if saveRaw:
            mac_dict[device.macAddress]['label'] = ['RAW' for i,elem in enumerate(mac_channels) if elem[0]==device.macAddress]
        else:
            mac_dict[device.macAddress]['label'] = [sensors[i] for i,elem in enumerate(mac_channels) if elem[0]==device.macAddress]
        
        aux = [10, 10, 10, 10, 6, 6]
        aux2 = [1 for elem in mac_channels if elem[0]==device.macAddress]
        mac_dict[device.macAddress]['resolution'] = [4] + [aux[i] for i in range(len(aux2))]
        resolution[device.macAddress] = mac_dict[device.macAddress]['resolution']

    header = {'resolution': resolution, 'saveRaw': saveRaw}
    
    print("# " + str(mac_dict) + '\n')
    filename.write("# " + str(mac_dict) + '\n')
    #filename.write('# {"20:16:07:18:16:69": {"sensor": ["RAW", "RAW", "RAW", "RAW", "RAW", "RAW"], "device name": "Device 1", "column": ["nSeq", "I1", "I2", "O1", "O2", "A1", "A2", "A3", "A4", "A5", "A6"], "sync interval": 2, "time": ' + file_time+', "comments": "", "device connection": "20:16:07:18:16:69", "channels": [1, 2, 3, 4, 5, 6], "date": '+file_date+', "mode": 0, "digital IO": [0, 0, 0, 0, 1, 1, 1, 1], "firmware version": "5.1", "device": "bitalino_rev", "position": 0, "sampling rate": 1000, "label": ["EDA", "BVP", "EMG", "Acc X", "Acc Y", "Acc Z"], "resolution": [4, 1, 1, 1, 1, 10, 10, 10, 10, 6, 6], "special": [{}, {}, {}, {}, {}, {}]}, "20:16:07:18:14:11": {"sensor": ["RAW", "RAW", "RAW", "RAW", "RAW", "RAW"], "device name": "Device 2", "column": ["nSeq", "I1", "I2", "O1", "O2", "A1", "A2", "A3", "A4", "A5", "A6"], "sync interval": 2, "time": ' + file_time + ', "comments": "", "device connection": "20:16:07:18:14:11", "channels": [1, 2, 3, 4, 5, 6], "date": ' + file_date + ', "mode": 0, "digital IO": [0, 0, 0, 0, 1, 1, 1, 1], "firmware version": "5.1", "device": "bitalino_rev", "position": 1, "sampling rate": 1000, "label": ["EOG", "ECG", "PZT", "Acc X", "Acc Y", "Acc Z"], "resolution": [4, 1, 1, 1, 1, 10, 10, 10, 10, 6, 6], "special": [{}, {}, {}, {}, {}, {}]}}' +'\n')
    filename.write('# EndOfHeader' + '\n')
    
    return tuple(fmt), header




