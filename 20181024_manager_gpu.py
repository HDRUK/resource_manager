#!/usr/bin/env python

import socket
import os
import subprocess

def currently_running():
    p = subprocess.Popen("ps -o pid,cmd -ef | grep -v defunct | sed 's/^ *//;s/ *$//' | cut -d ' ' -f 1 | sort -u", shell=True, stdout=subprocess.PIPE)
    p.wait()
    e, _ = p.communicate()
    return [int(i) for i in e.decode().split('\n') if i.isdigit()]

def resource_manager(TCP_IP='127.0.0.1', TCP_PORT=5013, devices=None):
    if devices is None:
        devices = { #the devices available for gpu in the server
            0: {'name': 'gpu0', 'path': '/gpu:0', 'available':True, 'pid_using': 0},
            1: {'name': 'gpu1', 'path': '/gpu:1', 'available':True, 'pid_using': 0},
            #2: {'name': 'gpu2', 'path': '/gpu:2', 'available':True, 'pid_using': 0}
        }
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #starts the socket
    s.bind((TCP_IP, TCP_PORT)) #this will bind to the settings given before. if TCP_IP is 127.0.0.1 it will only accept loopback connections
    s.listen(1)
    while 1: #will loop answering the clients
        print(devices)
        conn, addr = s.accept() #gets one client
        pids_running = currently_running()
        print('Connection: {}'.format(addr)) #print connected client (ip/port)
        while 1: #iteracts with this client
            data = conn.recv(512) #receive message with buffer_size 512
            if not data: #if failed stop)
                break
            print("Received: {}".format(data.decode())) #print received message
            signal, pid = data.decode().split(' ') #split the 'HELLO PID' message
            pid = int(pid)
            if signal == 'HELLO':
                if pid not in pids_running: #in case the pid received is not in the running list it indicates some problem
                    print("Process received is not running? {} not in ({})".format(pid, pids_running))
                    break
                else:
                    for i, info in devices.items(): #check if the device list has elements that stopped running
                        if not(info['available']):
                            pid_using = info['pid_using']
                            if pid_using not in pids_running:
                                info['available'] = True
                                info['pid_using'] = 0
                    device_is = -1
                    for i, info in devices.items(): #check if there is any device available, if so let's mark it
                        if info['available'] is True:
                            info['available'] = False
                            info['pid_using'] = pid
                            device_is = i
                            break
                    path = 'NONE' #default path
                    if device_is in devices.keys(): #if device_is is not -1 we have a path
                        path = devices[device_is]['path']
                    signal = True if path != 'NONE' else False #set the signal if we have a path
                    data = "{} {}".format(signal, path).encode("ASCII") #encode for transmission
                    print("Sending: {}".format(data)) #print the message that will be send
                    conn.send(data) #send the data
            elif signal == 'BYE':
                for i, info in devices.items():
                    if not(info['available']):
                        if info['pid_using'] == pid:
                            info['available'] = True
                            info['pid_using'] = 0
                conn.send('BYE BYE'.encode('ASCII'))
        conn.close() #close current client connection


if __name__ == '__main__':
    resource_manager()

