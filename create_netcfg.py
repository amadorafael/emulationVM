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

fixPortSpeed = 100 #Mbps
speeds = {}
test={}

def ovs(pName,pSpeed):
    if str(pSpeed) == str(100):
        rate = subprocess.run(['sudo', 'ovs-vsctl', 'set', 'interface',pName,'ingress_policing_rate=100000'], check=True, stdout=subprocess.PIPE, universal_newlines=True)
        # print(rate)
        # pause
        burst = subprocess.run(['sudo', 'ovs-vsctl', 'set', 'interface',pName,'ingress_policing_burst=80000'], check=True, stdout=subprocess.PIPE, universal_newlines=True)
        # print(burst)
    if str(pSpeed) == str(50):
        rate = subprocess.run(['sudo', 'ovs-vsctl', 'set', 'interface',pName,'ingress_policing_rate=50000'], check=True, stdout=subprocess.PIPE, universal_newlines=True)
        # print(rate)
        # pause
        burst = subprocess.run(['sudo', 'ovs-vsctl', 'set', 'interface',pName,'ingress_policing_burst=8000'], check=True, stdout=subprocess.PIPE, universal_newlines=True)
        # print(burst)




# # ------------------- Cleaning disconnected ------------------------ #
# devices = base_ONOS.readDevices (ctrl)
# for dev in devices:
#     status = str(devices[dev][2])
#     devNum = str(devices[dev][0])
#     try:
#         status.index('disconnected')
#     except ValueError:
#         print(status)
#     else:
#         print('Deleting device: ', devNum)
#         base_ONOS.deleteDevice ( devNum, ctrl )
# # ------------------------------------------------------------------ #


if __name__ == '__main__':
    # ---------------------- Switch Name netcfg file POST -------------------------- #
    devices = base_ONOS.readDevices (ctrl)
    for dev in devices:
        devNum = str(devices[dev][0])
        ports = base_ONOS.readPorts(devNum, ctrl)
        for port in ports:
            try:
                portNum = str(ports[port][1])
                portName = str(ports[port][3]["portName"])
                # print(portName, portNum)
                if portNum == 'local': 
                    # ---- config Device Names ONOS GUI ---- #
                    nameConfig = {"devices": {devNum: { "basic": { "name": portName  } } }}
                    print('Switch Name: '+portName)
                    base_ONOS.config_netcfg_POST (ctrl, nameConfig)
            except IndexError:
                pass


    # ---------------- Port Speeds Configuration | netcfg file POST ------------------

    edgesInfo = {}

    # - READING EDGES AND NODES FROM OVS GENERATOR -
    # --------------- Read EDGES -------------------
    with open('windows-edge.json') as f:
        edge_data = json.load(f)

    # ----------- Read NODES -----------------
    with open('windows-node.json') as f:
        node_data = json.load(f)

    edgeCount = 0
    for edge in edge_data:
        linkFROM = str(edge_data[edge]['from'])
        linkID = str(edge_data[edge]['id'])
        for node in node_data:
            nodeID = str(node_data[node]['id'])
            if nodeID == linkFROM:
                nodeNAME = str(node_data[node]['label'])
                edgesInfo[edgeCount] = {'id': linkID, 'from': nodeNAME}
                linkTO = str(edge_data[edge]['to'])
                for node in node_data:
                    nodeID = str(node_data[node]['id'])
                    nodeNAME = str(node_data[node]['label'])
                    if nodeID == linkTO:
                        try:
                            linkSPEED = str(edge_data[edge]['label'])
                            edgesInfo[edgeCount].update({'to': nodeNAME, 'speed': linkSPEED})
                            edgeCount = edgeCount+1
                        except KeyError:
                            pass

    print(edgesInfo)

    # -------- Edges data formatting ----------------

    LinkTopologyMatrix = []
    for edge in edgesInfo:
        try:
                                        # ID                    FROM                        TO                  SPEED           ctrl_PORT_NUM
            LinkTopologyMatrix.append([edgesInfo[edge]['id'], edgesInfo[edge]['from'],edgesInfo[edge]['to'],edgesInfo[edge]['speed'],0])
        except KeyError:
            pass

    PortNamesMatrix = []
    devices = base_ONOS.readDevices (ctrl)
    for dev in devices:
        devNum = str(devices[dev][0])
        ports = base_ONOS.readPorts(devNum, ctrl)
        for port in ports:
            try:
                portNum = str(ports[port][1])
                portName = str(ports[port][3]["portName"])
                if portNum != 'local' and len(portName) > 7:
                    #                          Port _flag
                    PortNamesMatrix.append([portName, 0, portNum, devNum])
            except KeyError:
                pass
    
    # print(PortNamesMatrix)
    LinkTopologyMatrix_edited = []
    for top in LinkTopologyMatrix:
        notFoundFlag = True
        speed_link = top[3]
        for idx, port in enumerate(PortNamesMatrix):
            if notFoundFlag:
                port_address = port[0][2:11]  #sw00-sw01
                port_value = port[0][-1]      #1
                portNameEnum = port[0]
                _flag = port[1]
                port_from_to = top[1]+'-'+top[2]

                if (port_from_to == port_address) and (_flag == 0):
                    PortNamesMatrix[idx][1] = 1
                    top[4] = port_value
                    portNUM = PortNamesMatrix[idx][2]
                    devNUM = PortNamesMatrix[idx][3]
                    LinkTopologyMatrix_edited.append([devNUM, portNameEnum, portNUM, speed_link])
                    notFoundFlag = False

    # Link/Ports/Speed matrix
    print('# ---------- Link Speeds ------------- #')
    print('# [Device, Port Name, Port Number, Speed] #')
    print(LinkTopologyMatrix_edited)
    print('# -------------- netcfg file POST / Ingress Policies --------#')
    # Finding the remote ports and POST:
    for port in LinkTopologyMatrix_edited:
        devNum = port[0]
        portNum = port[2]
        portSpeed = port[3]
        portConfig = {"devices": {str(devNum): { "ports": { str(portNum): { "number": portNum, "speed": portSpeed } } } },"ports": {str(devNum)+"/"+str(portNum): {"bandwidthCapacity": { "capacityMbps": portSpeed } } }}
        # print('SOURCE')
        print('-------------------------')
        # print(portConfig)
        base_ONOS.config_netcfg_POST (ctrl, portConfig)

        ## Ingress Policies config
        ovs(portName,portSpeed)

        linksONOS = base_ONOS.readLinks(ctrl)
        for link in linksONOS:
            srcPort = linksONOS[link][0]['port']
            srcDevice = linksONOS[link][0]['device']
            dstDevice = linksONOS[link][1]['device']
            dstPort = linksONOS[link][1]['port']
            # print(srcDevice,srcPort,'--',dstDevice,dstPort)
            if str(devNum) == str(srcDevice) and str(portNum) == str(srcPort):
                print(srcDevice,srcPort,'--',dstDevice,dstPort,' | ',portSpeed)
                portConfig = {"devices": {str(dstDevice): { "ports": { str(dstPort): { "number": dstPort, "speed": portSpeed } } } },"ports": {str(dstDevice)+"/"+str(dstPort): {"bandwidthCapacity": { "capacityMbps": portSpeed } } }}
                # print('DESTINATION')
                # print(portConfig)
                base_ONOS.config_netcfg_POST (ctrl, portConfig)

                portsDst = base_ONOS.readPorts(dstDevice, ctrl)
                for port in portsDst:
                    portNumDst = str(portsDst[port][1])
                    portNameDst = str(portsDst[port][3]["portName"])
                    if portNumDst == dstPort:
                        # print(portNameDst)

                        ## Ingress Policies config
                        ovs(portNameDst,portSpeed)
            
            if str(devNum) == str(dstDevice) and str(portNum) == str(dstPort):
                print(srcDevice,srcPort,'--',dstDevice,dstPort,' | ',portSpeed)
                portConfig = {"devices": {str(srcDevice): { "ports": { str(srcPort): { "number": srcPort, "speed": portSpeed } } } },"ports": {str(srcPort)+"/"+str(srcPort): {"bandwidthCapacity": { "capacityMbps": portSpeed } } }}
                # print('DESTINATION')
                # print(portConfig)
                base_ONOS.config_netcfg_POST (ctrl, portConfig)

                portsSrc = base_ONOS.readPorts(srcDevice, ctrl)
                for port in portsSrc:
                    portNumSrc = str(portsSrc[port][1])
                    portNameSrc = str(portsSrc[port][3]["portName"])
                    if portNumSrc == srcPort:
                        # print(portNameDst)

                        ## Ingress Policies config
                        ovs(portNameSrc,portSpeed)
            


print('#---------------------------------------------------#')
print('# If no link speed is defined in OVS Generator,     #')
print('# ports will receive the standard bandwidth: 10Gbps #')
print('#---------------------------------------------------#')


