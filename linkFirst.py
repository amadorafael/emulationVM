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
import subprocess

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

link_id = {}
devices = base_ONOS.readDevices (ctrl)
for dev in devices:
    devNum = str(devices[dev][0])
    ports = base_ONOS.readPorts(devNum, ctrl)
    for port in ports:
        portNum = str(ports[port][1])
        portName = str(ports[port][3]["portName"])
        if portNum != 'local' and len(portName) > 7:
            # print(portName[len(portName)-1])
            
            # if int(portName[len(portName)-1]) > 1:
            for edge in edgesInfo:
                try:
                    edgePortFWD = 'c.'+edgesInfo[edge]['from']+'-'+edgesInfo[edge]['to']
                    portSpeed = edgesInfo[edge]['speed']
                    # print(portName)
                    if 'portName' in edgesInfo:
                        if str(edgePortFWD) == str(portName[:-2]) and edgesInfo[edge]['portName'] != portName:
                            # edgesInfo[linkID] = {'from': nodeNAME}
                            # link_id[edge].update({'port': edgePortFWD})
                            edgesInfo[edge].update({'portName': portName})
                            # print(link_id)
                    else:
                        if str(edgePortFWD) == str(portName[:-2]):
                            edgesInfo[edge].update({'portName': portName})
                    
                    
                except:
                    pass
                
                # print(set(link_id))

# print(set(link_id))
# print(link_id)

# for i in link_id:
#     print(i,link_id[i])

print('--------------- TEstingssss ----------------')


# print(edgesInfo)

for edge in edgesInfo:
    print(edgesInfo[edge])
# edgesControl = edgesInfo.copy()

print('--------------- ---- ----------------')


# link_id = []

linksONOS = base_ONOS.readLinks(ctrl)
for link in linksONOS:
    srcPort = linksONOS[link][0]['port']
    srcDevice = linksONOS[link][0]['device']
    dstDev = linksONOS[link][1]['device']
    dstPort = linksONOS[link][1]['port']

    devices = base_ONOS.readDevices (ctrl)
    for dev in devices:
        devNum = str(devices[dev][0])
        ports = base_ONOS.readPorts(devNum, ctrl)
        for port in ports:
            portNum = str(ports[port][1])
            portName = str(ports[port][3]["portName"])
            if str(devices[dev][0]) == str(srcDevice) and str(portNum) == str(srcPort): # Correspondence between link/ports
                link_id = []
                for edge in edgesInfo:
                    try:
                        edgePortFWD = 'c.'+edgesInfo[edge]['from']+'-'+edgesInfo[edge]['to']
                        portSpeed = edgesInfo[edge]['speed']
                        if str(edgePortFWD) == str(portName[:-2]):
                            print(portName, portSpeed, edge)
                            # link_id.append(edge)
                    except:
                        pass

                    # print(link_id)

                # print('Source Port: '+portName)
                portsDst = base_ONOS.readPorts(dstDev, ctrl)
                for port in portsDst:
                    portNumDst = str(portsDst[port][1])
                    portNameDst = str(portsDst[port][3]["portName"])
                    if portNumDst == dstPort:
                        print('Source Port: '+portName+' - '+srcPort+' | '+'Destination Port: '+portNameDst+' - '+dstPort)

            # ctrl_id = ''
            # for edge in edgesInfo:
            #         try:
            #             edgePortFWD = 'c.'+edgesInfo[edge]['from']+'-'+edgesInfo[edge]['to']
            #             portSpeed = edgesInfo[edge]['speed']
            #             if str(edgePortFWD) == str(portName[:-2]):
            #                 if ctrl_id == edge:
            #                     break
            #                 print(portName, portSpeed, edge)
            #                 ctrl_id = edge
            #                 # link_id.append(edge)
            #         except:
            #             pass
    