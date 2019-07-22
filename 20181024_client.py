#!#!/usr/bin/env python

import socket
import os
import time


def try_resource(blocking = False, sleep_time = 60, TCP_IP='127.0.0.1', TCP_PORT=5011):
    '''
        this function will query for an available resource in the server
        blocking: if this function should loop until we get an available device
        sleep_time: the time in seconds to sleep until next try
    '''
    if sleep_time <= 0: #let's have a minimum amount of time so we don't overload
        sleep_time = 5
    signal = False
    path = "NONE"
    while not signal: #while we don't have signal or exit
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #setup tcp
            s.connect((TCP_IP, TCP_PORT)) #connect to the manager
            MESSAGE = "HELLO {}".format(os.getpid()).encode("ASCII") #prepare message
            s.send(MESSAGE) #send message
            data = s.recv(512) #receive manager message with buffer_size 512
            s.close() #close the tcp connection
        except Exception as e: # if the tcp connection fails report it
            print(e)
            if not blocking: #if it is not blocking return failed
                return False, "ERROR"
            time.sleep(sleep_time) #sleep before trying again
            continue #otherwise will try again
        signal, path = data.decode().split(' ') #decode output
        signal = signal.lower() in ["true", "yes"] #convert from str to bool
        if not blocking or signal: #if not blocking exit the loop
            return signal, path #return the answer
        time.sleep(sleep_time) #sleep some time if we are waiting for an available device
    return signal, path #if it was blocking this will return some signal


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






