#!#!/usr/bin/env python

import socket
import os
import time


def _send_message(blocking, sleep_time, TCP_IP, TCP_PORT, MESSAGE):
    signal = False
    PATH = 'NONE'
    if sleep_time <= 0: #let's have a minimum amount of time so we don't overload
        sleep_time = 5
    while not signal: #while we don't have signal or exit
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #setup tcp
            s.connect((TCP_IP, TCP_PORT)) #connect to the manager
            s.send(MESSAGE.encode('ASCII')) #send message
            data = s.recv(512) #receive manager message with buffer_size 512
            signal, path = data.decode().split(' ') #decode output
            signal = signal.lower() in ["true", "yes"] #convert from str to bool
            s.close() #close the tcp connection
        except Exception as e: # if the tcp connection fails report it
            print(e)
            if not blocking: #if it is not blocking return failed
                return False, "ERROR"
            time.sleep(sleep_time) #sleep before trying again
            continue #otherwise will try again
        if not blocking or signal: #if not blocking exit the loop
            return signal, path #return the answer
        time.sleep(sleep_time) #sleep some time if we are waiting for an available device
    return signal, path

def try_resource(blocking = False, sleep_time = 60, TCP_IP='127.0.0.1', TCP_PORT=5013):
    '''
        this function will query for an available resource in the server
        blocking: if this function should loop until we get an available device
        sleep_time: the time in seconds to sleep until next try
    '''
    signal = False
    path = "NONE"
    MESSAGE = "HELLO {}".format(os.getpid())
    signal, path = _send_message(blocking, sleep_time, TCP_IP, TCP_PORT, MESSAGE)
    return signal, path #if it was blocking this will return some signal

def release_resource(TCP_IP='127.0.0.1', TCP_PORT=5013):
    _send_message(blocking=False, sleep_time=5, TCP_IP=TCP_IP, TCP_PORT=TCP_PORT, MESSAGE='BYE {}'.format(os.getpid()))

if __name__ == '__main__':
    print(try_resource(True, 5))
    time.sleep(5)


#to be used with:
"""from keras import backend as K
import tensorflow as tf

signal, device_path = try_resource(True)

with K.tf.device(device_path):
    config = tf.ConfigProto(intra_op_parallelism_threads=4,\
           inter_op_parallelism_threads=4, allow_soft_placement=True,\
           device_count = {'CPU' : 1, 'GPU' : 1})
    session = tf.Session(config=config)
    K.set_session(session)"""






