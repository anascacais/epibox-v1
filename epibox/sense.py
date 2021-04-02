# local
from open_file_sense import open_file
from start_system_sense import start_system
from read_modules_sense import read_modules
from scientisst import *

# epibox
from epibox import header2bitalino
from epibox import create_folder

#third-party
from scipy import signal
import numpy as np
import paho.mqtt.client as mqtt

#built-in
import json
import ast
from subprocess import Popen, PIPE, run, call
import time
import string
import random

#opt = {'initial_dir': '/home/pi/Documents/dev', 'patient_id': 'sense', 'fs': 1000, 'devices_mac': ['AC:67:B2:1E:83:1A'], 'channels': [['AC:67:B2:1E:83:1A', '1', '-'], ['AC:67:B2:1E:83:1A', '2', '-'], ['AC:67:B2:1E:83:1A', '3', '-'], ['AC:67:B2:1E:83:1A', '4', '-'], ['AC:67:B2:1E:83:1A', '5', '-'], ['AC:67:B2:1E:83:1A', '6', '-']]}

def random_str(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))

def on_message(client, userdata, message):
    
    message = str(message.payload.decode("utf-8"))
    message = ast.literal_eval(message)
    #print("message received: ", message)
    
    if message[0] == 'RESTART':
        client.loop_stop()
        from epibox import mqtt_startup
        mqtt_startup.main()
        
    elif message[0] == 'INTERRUPT':
        client.keepAlive = False
    
    elif message[0] == 'PAUSE ACQ':
        print('PAUSING ACQUISITION')
        global pause_acq
        pause_acq = True
        
    elif message[0] == 'RESUME ACQ':
        print('RESUMING ACQUISITION')
        pause_acq = False
        
    elif message[0] == 'ANNOTATION':
        print('RECEIVED ANNOT {} ----------------------'.format(message[1]))
        global new_annot
        global write_annot
        new_annot = message[1]
        write_annot = True

#****************************** MAIN SCRIPT ***********************************

def main():
    
    try:
    
        call(['rfkill', 'block', 'bluetooth'])
        call(['rfkill', 'unblock', 'bluetooth'])
        
        # SET INITIAL VARIABLES ===============================================================
        
        with open('/home/pi/Documents/epibox/args.json', 'r') as json_file:
            opt = json_file.read()
        opt = ast.literal_eval(opt)
        
        client_name = random_str(6)
        print('Client name (acquisition):', client_name)
        host_name = '192.168.0.10'
        topic = 'rpi'
        
        client = mqtt.Client(client_name)
        setattr(client, 'keepAlive', True)
        client.username_pw_set(username='preepiseizures', password='preepiseizures')
        client.connect(host_name)
        client.subscribe(topic)
        client.on_message = on_message
        client.loop_start()
        print('Successfully subcribed to topic', topic)
        init = False
        client.publish('rpi', "['STARTING']")
         

        device = Sense(opt['devices_mac'][0])
        devices = [device]

        if not opt['channels']:
            channels = []
            for device in opt['devices_mac']:
                for i in range(1,7):
                    channels += [[device,str(i)]]
            sensors = ['-' for i in range(len(channels))]

        else:
            channels = []
            sensors = []
            for triplet in opt['channels']:
                channels += [triplet[:2]] 
                sensors += [triplet[2]]
                
        # transform list of channels into string
        channels_str = []
        for pair in channels:
            channels_str += str(int(pair[1])-1)
        channels_str = ' '.join(channels_str)
        
        saveRaw = bool(opt['saveRaw'])
        service = opt['service']
        
        global write_annot
        global new_annot
        global pause_acq
        write_annot = False
        pause_acq = False
        already_notified_pause = False
        
        print('ID: {}'.format(opt['patient_id']))
        print('folder: {}'.format(opt['initial_dir']))
        print('fs: {}'.format(opt['fs']))
        print('saveRaw: {}'.format(saveRaw))
        print('channels: {}'.format(channels))
        print('devices: {}'.format(opt['devices_mac']))
        print('sensors: {}'.format(sensors))
        
        
        # PAIR DEVICE IF NOT ALREADY ===============================================================
        
#         paired_devices = run(['bluetoothctl', 'paired-devices'], capture_output=True, text=True).stdout.split('\n')
#         paired = [mac in [p.split()[1] for p in paired_devices[:-1]] for mac in opt['devices_mac']]
#         
#         if not all(paired):
#             client.publish('rpi', "['PAIRING']")
#             
#         already_timed_out = False
#         init_connect_time = time.time()
#         
#         while not all(paired):
#             
#             if (time.time() - init_connect_time) > 120 or client.keepAlive == False:
#                 client.publish('rpi', "['STOPPED']")
#                 client.loop_stop()
#                 print('TIMEOUT')
#                 # Disconnect the system
#                 client.keepAlive = False
#                 pass
#             
#     
#             if already_timed_out == True and time.time() - init_connect_time > 10:
#                 already_timed_out = False
#                     
#             for imac,mac in enumerate(opt['devices_mac']):
#                 
#                 if not paired[imac]:
#                     print('Trying to pair {}'.format(mac))
#                     try:
#                         child = pexpect.spawn('bluetoothctl')
#                         child.expect('#')
#                         child.sendline('default agent')
#                         child.expect('#')
#                         child.sendline('scan on')
#                         child.expect('#')
#                         child.sendline('pair {}'.format(mac))
#                         child.expect('Confirm passkey')
#                         child.sendline('yes')
#                         
#                         print('Successfully paired {}!'.format(mac))
#                         paired[imac] = True
#                         
#                     except Exception as e:
#                         print(e)
#                         if already_timed_out == False and time.time() - init_connect_time > 10:
#                             timeout_json = json.dumps(['TIMEOUT', '{}'.format(mac)])
#                             client.publish('rpi', timeout_json)
#                             print('SENT TIMEOUT')
#                             already_timed_out = True
#                             init_connect_time = time.time()
        
        # Use/create the patient folder ===============================================================
        
        directory = create_folder.create_folder(opt['initial_dir'], opt['patient_id'], service)
        
        # Starting Acquisition LOOP =========================================================================
        
        try:
        
            while client.keepAlive == True:
                
                try:
                    a_file, annot_file, drift_log_file, save_fmt, header = open_file(directory, devices, channels, sensors, opt['fs'], saveRaw)

                except Exception as e:
                    print(e)
                    
                try:
                    sync_param = start_system()
                except Exception as e:
                    print(e)
                
                print(['/home/pi/Documents/sense/test', opt['devices_mac'][0], channels_str, str(opt['fs']), a_file.name, drift_log_file])
                process = Popen(['/home/pi/Documents/sense/test', opt['devices_mac'][0], channels_str, str(opt['fs']), a_file.name, drift_log_file], stdout=PIPE, stdin=PIPE, shell=False)
                
                data = np.array([])
                
                while client.keepAlive == True:
                    
                    bOutput = process.stdout.readline()
                    
#                     if bOutput == '': # and process.poll() is not None:
#                         print('breaking')
#                         break
                    
                    if bOutput:
                        
                        output = bytes.decode(bOutput.strip())
                        
                        if output.split(',')[0] == 'DATA':
                            
                            print(output)
                            
                            output = output.split(',')[1].split(' ')
                            output = np.array(list(map(int,output)))
                            
                            if data.size == 0:
                                data = output
                            else:
                                data = np.vstack((data, np.array(output)))
                            
                            if data.shape[0] == 100:
                                t_disp = read_modules(data, devices, channels, sensors, header)
                                data = np.array([])
                                
                                t_display = []
                                if opt['fs'] == 1000:# changes sampling rate to 100 (if larger)
                                    for i in range(t_disp.shape[1]):
                                        t_display += [signal.decimate(t_disp[:,i], 10).tolist()]
                                else:
                                    for i in range(t_disp.shape[1]):
                                        t_display += [t_disp[:,i].tolist()]  
                                            
                                json_data = json.dumps(['DATA', t_display, channels, sensors])
                                client.publish('rpi', json_data)
                                already_timed_out = False
                                
      
                        else:
                            print(output)
                        
                    if time.time()-sync_param['inittime'] > 60*60:
                         print('1 hour has passed - closing and initiating another round')
                         process.communicate(input=b'\n')
                         break 
        
            print('')
            print('You have stopped the acquistion. Saving all the files ...')
            client.publish('rpi', "['STOPPED']")
            client.loop_stop()
            
            # Disconnect the system
            try:
                process.communicate(input=b'\n')
            except Exception as e:
                print(e)
                
            client.keepAlive == False
            pass
            
            print('You have stopped the acquistion. Saving all the files ...')
            time.sleep(3)
            pid = run(['sudo', 'pgrep', 'python'], capture_output=True, text=True).stdout.split('\n')[:-1]
            for p in pid:
                run(['kill', '-9', p])
        
        except KeyboardInterrupt:
            print('')
            print('You have stopped the acquistion. Saving all the files ...')
            client.publish('rpi', "['STOPPED']")
            client.loop_stop()
            
            # Disconnect the system
            try:
                process.communicate(input=b'\n')
            except Exception as e:
                print(e)
                
            client.keepAlive == False
            pass
            
    except Exception as e:
        print(e)
        client.publish('rpi', "['STOPPED']")
        client.loop_stop()
        
        # Disconnect the system
        print('You have stopped the acquistion. Saving all the files ...')
        time.sleep(3)
        pid = run(['sudo', 'pgrep', 'python'], capture_output=True, text=True).stdout.split('\n')[:-1]
        for p in pid:
            run(['kill', '-9', p])
        

if __name__ == '__main__':

    main()