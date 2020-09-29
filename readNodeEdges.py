#!/usr/bin/python3

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
        
edgesInfo = {}
aux = {}


# - READING EDGES AND NODES FROM OVS GENERATOR -
# --------------- Read EDGES -------------------
with open('windows-edge.json') as f:
    edge_data = json.load(f)

# ----------- Read NODES -----------------
with open('windows-node.json') as f:
    node_data = json.load(f)

for edge in edge_data:
    linkFROM = str(edge_data[edge]['from'])
    linkID = str(edge_data[edge]['id'])
    for node in node_data:
        nodeID = str(node_data[node]['id'])
        if nodeID == linkFROM:
            nodeNAME = str(node_data[node]['label'])
            edgesInfo[linkID] = {'from': nodeNAME}
            linkTO = str(edge_data[edge]['to'])
            for node in node_data:
                nodeID = str(node_data[node]['id'])
                nodeNAME = str(node_data[node]['label'])
                if nodeID == linkTO:
                    try:
                        linkSPEED = str(edge_data[edge]['label'])
                        edgesInfo[linkID].update({'to': nodeNAME, 'speed': linkSPEED})
                    except KeyError:
                        pass


# print(edgesInfo)
# for i in edgesInfo:
#     try:
#         edgePorts = 'c.'+edgesInfo[i]['from']+'-'+edgesInfo[i]['to']
#         portSpeed = edgesInfo[i]['speed']
#         print(edgePorts, portSpeed)
#     except KeyError:
#         pass 


devices = base_ONOS.readDevices (ctrl)
for dev in devices:
    devNum = str(devices[dev][0])
    ports = base_ONOS.readPorts(devNum, ctrl)
    for port in ports:
        portNum = str(ports[port][1])
        portName = str(ports[port][3]["portName"])
        if portNum != 'local' and len(portName) > 7 :
            if int(portName[len(portName)-1]) == 1:  # only one interface in the same port ex: 'c.sw00-sw01.1'
                for i in edgesInfo:
                    try:
                        # Check portNames vs Edges Info - one direction
                        edgePortsFWD = 'c.'+edgesInfo[i]['from']+'-'+edgesInfo[i]['to']
                        portSpeed = edgesInfo[i]['speed']
                        # print('CheckPoint FWD')
                        # print(edgePortsFWD, portName[:-2])
                        if str(edgePortsFWD) == str(portName[:-2]):
                            portConfig = {"devices": {str(devNum): { "ports": { str(portNum): { "number": portNum, "speed": portSpeed } } } },"ports": {str(devNum)+"/"+str(portNum): {"bandwidthCapacity": { "capacityMbps": portSpeed } } }} # MUST ADAPT TO READ FILE WITH LINKS FROM OVS-MESH
                            print(portConfig)
                            # base_ONOS.config_netcfg_POST (ctrl, portConfig)

                        # Check portNames vs Edges Info - other direction
                        edgePortsRET = 'c.'+edgesInfo[i]['to']+'-'+edgesInfo[i]['from']
                        portSpeed = edgesInfo[i]['speed']
                        # print('CheckPoint RET')
                        # print(edgePortsRET, portName[:-2])
                        if str(edgePortsRET) == str(portName[:-2]):
                            portConfig = {"devices": {str(devNum): { "ports": { str(portNum): { "number": portNum, "speed": portSpeed } } } },"ports": {str(devNum)+"/"+str(portNum): {"bandwidthCapacity": { "capacityMbps": portSpeed } } }} # MUST ADAPT TO READ FILE WITH LINKS FROM OVS-MESH
                            print(portConfig)
                            # base_ONOS.config_netcfg_POST (ctrl, portConfig)
                    except KeyError:
                        pass               
            else:
                print('More than one interface in this port')
