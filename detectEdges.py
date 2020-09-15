#!/usr/bin/python3

###################################################################
# Rafael George Amado - ETS
# 2020-09-11
###################################################################

# imports
import json, requests, sys, time, os
from datetime import datetime
import pce
import base_ONOS
import docker

# edge = sys.argv[0]
# print(edge)

# Get ONOS container IP address
client = docker.DockerClient()
container = client.containers.get('onos')
ctrlIP = container.attrs['NetworkSettings']['IPAddress']

ctrl = 'http://'+ctrlIP+':8181/onos/v1/'

devices = base_ONOS.readDevices (ctrl)
for dev in devices:
    devNum = str(devices[dev][0])
    ports = base_ONOS.readPorts(devNum, ctrl)
    for port in ports:
        portNum = str(ports[port][1])
        portName = str(ports[port][3]["portName"])
        print(portNum)
        # print(portName, portName)
        # print(edge)
        if portNum != 'local':       
            try:
                portName.index('host00')
            except ValueError:
                # print('Not Found')
                pass
            else:
                print(devNum)
                # pass

# sys.exit(found)