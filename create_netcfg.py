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

# - READING EDGES AND NODES FROM OVS GENERATOR -
# --------------- Read EDGES -------------------
with open('windows-edge.json') as f:
    edge_data = json.load(f)

for edge in edge_data:
    linkId = str(edge_data[edge]['id'])
    linkFrom = str(edge_data[edge]['from'])
    linkTo = str(edge_data[edge]['to'])

    try:
        linkSpeed = str(edge_data[edge]['label'])
    except KeyError:
        # print('Link '+linkId+' has no link speed data')
        linkSpeed = 'NotSpecified'
        pass

    print(linkId, linkFrom, linkTo, linkSpeed)


# ----------- Read NODES -----------------
with open('windows-node.json') as f:
    node_data = json.load(f)

for node in node_data:
    nodeLabel = str(node_data[node]['label'])
    nodeId = str(node_data[node]['id'])
    print(nodeId, nodeLabel)






# ---------------------- netcfg file POST -------------------------- #
devices = base_ONOS.readDevices (ctrl)
for dev in devices:
    devNum = str(devices[dev][0])
    ports = base_ONOS.readPorts(devNum, ctrl)
    for port in ports:
        portNum = str(ports[port][1])
        portName = str(ports[port][3]["portName"])
        print(portName, portNum)
        if portNum == 'local': 
            # print('LOCALLLLLLLLLLLL')
            # ---- config Device Names ONOS GUI ---- #
            nameConfig = {"devices": {devNum: { "basic": { "name": portName  } } }}
            print('Switch Name: '+portName)
            base_ONOS.config_netcfg_POST (ctrl, nameConfig)
        
        else: 
            # ------ Fixed Link Speeds - 100Mbps ------
            # print('portNum: '+portNum)
            # print('portName: '+portName)
            # portConfig = {"ports": { str(devNum+"/"+portNum) : { "bandwidthCapacity": { "capacityMbps": 50 }}}}
            # print('POSTTTTTTTTTTTTTTTTTTTTTTTTT')
            portConfig = {"devices": {str(devNum): { "ports": { str(portNum): { "number": portNum, "speed": fixPortSpeed } } } },"ports": {str(devNum)+"/"+str(portNum): {"bandwidthCapacity": { "capacityMbps": fixPortSpeed } } }} # MUST ADAPT TO READ FILE WITH LINKS FROM OVS-MESH
            base_ONOS.config_netcfg_POST (ctrl, portConfig)

            # if portName in speeds:
            #     try:
            #         speeds[portName].append[fixPortSpeed]
            #     except:
            #         pass
            # else:
            #     speeds[portName] = fixPortSpeed

## Link Speeds 
# with open('speeds.json', 'w') as outfile:
    # json.dump(test, outfile)


        # config2 = {"devices": {str(devNum): { "ports": { str(portNum): { "number": 1, "speed": 100 } } } },"ports": {str(devNum)+"/"+str(portNum): {"bandwidthCapacity": { "capacityMbps": 100 } } }}
        # base_ONOS.config_netcfg_POST (ctrl, config2)
