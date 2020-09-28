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
        


# ----------- Read EDGES -----------------
with open('windows-edge.json') as f:
    edge_data = json.load(f)

for edge in edge_data:
    linkSpeed = str(edge_data[edge]['label'])
    linkId = str(edge_data[edge]['id'])
    linkFrom = str(edge_data[edge]['from'])
    linkTo = str(edge_data[edge]['to'])
    print(linkId, linkFrom, linkTo, linkSpeed)


# ----------- Read NODES -----------------
with open('windows-node.json') as f:
    node_data = json.load(f)

for node in node_data:
    nodeLabel = str(node_data[node]['label'])
    nodeId = str(node_data[node]['id'])
    print(nodeId, nodeLabel)

