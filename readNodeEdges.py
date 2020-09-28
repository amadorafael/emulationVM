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


# devices = base_ONOS.readDevices (ctrl)
# for dev in devices:
#     devNum = str(devices[dev][0])
#     ports = base_ONOS.readPorts(devNum, ctrl)
#     for port in ports:
#         portNum = str(ports[port][1])
#         portName = str(ports[port][3]["portName"])
#         print(portName, portNum)
        
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
    # linkSPEED = str(edge_data[edge]['label'])
    for node in node_data:
        nodeID = str(node_data[node]['id'])
        if nodeID == linkFROM:
            nodeNAME = str(node_data[node]['label'])
            edgesInfo[linkID] = {'from': nodeNAME}
            # print('from: '+str(node_data[node]['label']))
            linkTO = str(edge_data[edge]['to'])
            # print(linkTO)
            for node in node_data:
                nodeID = str(node_data[node]['id'])
                nodeNAME = str(node_data[node]['label'])
                if nodeID == linkTO:
                    try:
                        linkSPEED = str(edge_data[edge]['label'])
                        edgesInfo[linkID].update({'to': nodeNAME, 'speed': linkSPEED})

                    except KeyError:
                        pass
                    # try:
                    #     nodeLabel.index('sw')
                    # except ValueError:
                    #     pass
                    # else:
                    #     print('speed: '+str(edge_data[edge]['label']))

print(edgesInfo)