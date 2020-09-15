#!/usr/bin/python3

###################################################################
# Rafael George Amado - ETS
# 2020-09-14
###################################################################
# Create netcfg configuration and POST to ONOS

# imports
import json, requests, sys, time, os
import os.path
from datetime import datetime
import pce
import base_ONOS
import docker

# Get ONOS container IP address
client = docker.DockerClient()
container = client.containers.get('onos')
ctrlIP = container.attrs['NetworkSettings']['IPAddress']

ctrl = 'http://'+ctrlIP+':8181/onos/v1/'

fixPortSpeed = 100 #Mbps
speeds = {}
test={}

# ------------------- Cleaning disconnected ------------------------ #
devices = base_ONOS.readDevices (ctrl)
for dev in devices:
    status = str(devices[dev][2])
    devNum = str(devices[dev][0])
    try:
        status.index('disconnected')
    except ValueError:
        # print(status)
        pass
    else:
        print('Deleteing disconnected devices')
        print('Deleting device: ', devNum)
        base_ONOS.deleteDevice ( devNum, ctrl )