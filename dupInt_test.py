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
        print(rate)
        # pause
        burst = subprocess.run(['sudo', 'ovs-vsctl', 'set', 'interface',pName,'ingress_policing_burst=80000'], check=True, stdout=subprocess.PIPE, universal_newlines=True)
        print(burst)
    if str(pSpeed) == str(50):
        rate = subprocess.run(['sudo', 'ovs-vsctl', 'set', 'interface',pName,'ingress_policing_rate=50000'], check=True, stdout=subprocess.PIPE, universal_newlines=True)
        print(rate)
        # pause
        burst = subprocess.run(['sudo', 'ovs-vsctl', 'set', 'interface',pName,'ingress_policing_burst=8000'], check=True, stdout=subprocess.PIPE, universal_newlines=True)
        print(burst)

# def findIds (edgeData, nodeData):
#     for edge in edgeData:
#     fr1 = str(edgeData[edge]['from'])
#     to1 = str(edgeData[edge]['to'])
#     id1 = str(edgeData[edge]['id'])
#     for edge2 in edgeData:
#         fr2 = str(edgeData[edge2]['from'])
#         to2 = str(edgeData[edge2]['to'])
#         id2 = str(edgeData[edge2]['id'])
#         if fr1 == fr2 and to1 == to2 and id1 != id2:
#             print('Two interfaces')
#             print(str(nodeData[fr1]['label'])+'-'+str(nodeData[to1]['label']), id1, str(edgeData[edge]['label']))
                
def getPortNum (portSearchName):
        devices = base_ONOS.readDevices (ctrl)
        for dev in devices:
            devNum = str(devices[dev][0])
            ports = base_ONOS.readPorts(devNum, ctrl)
            for port in ports:
                portNum = str(ports[port][1])
                portName = str(ports[port][3]["portName"])
                if portName == portSearchName:
                    print(portNum)


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
            portNum = str(ports[port][1])
            portName = str(ports[port][3]["portName"])
            # print(portName, portNum)
            if portNum == 'local': 
                # ---- config Device Names ONOS GUI ---- #
                nameConfig = {"devices": {devNum: { "basic": { "name": portName  } } }}
                print('Switch Name: '+portName)
                base_ONOS.config_netcfg_POST (ctrl, nameConfig)
            
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


    # print(edgesInfo)

    LinkTopologyMatrix = []

    for edge in edgesInfo:
                                    # ID                    FROM                        TO                  SPEED                 PORT_NUM
        LinkTopologyMatrix.append([edgesInfo[edge]['id'], edgesInfo[edge]['from'],edgesInfo[edge]['to'],edgesInfo[edge]['speed'],0])
        # print(LinkTopologyMatrix)

    # print(LinkTopologyMatrix)

    PortNamesMatrix = []

    devices = base_ONOS.readDevices (ctrl)
    for dev in devices:
        devNum = str(devices[dev][0])
        ports = base_ONOS.readPorts(devNum, ctrl)
        for port in ports:
            portNum = str(ports[port][1])
            portName = str(ports[port][3]["portName"])
            if portNum != 'local' and len(portName) > 7:
                #                          Port    _flag
                PortNamesMatrix.append([portName, 0, portNum, devNum])
    
    # print(PortNamesMatrix)

    LinkTopologyMatrix_edited = []

    for top in LinkTopologyMatrix:
        notFoundFlag = True
        speed_link = top[3]
        # print(speed_link)
    
        for idx, port in enumerate(PortNamesMatrix):
            if notFoundFlag:
                port_address = port[0][2:11]  #sw00-sw01
                port_value = port[0][-1]      #1
                portNameEnum = port[0]

                _flag = port[1]
                port_from_to = top[1]+'-'+top[2]

                if (port_from_to == port_address) and (_flag == 0):
                    # print(port_from_to, port_address, speed_link)
                    PortNamesMatrix[idx][1] = 1
                    top[4] = port_value
                    portNUM = PortNamesMatrix[idx][2]
                    devNUM = PortNamesMatrix[idx][3]
                    #speed_link = top[3]
                    # LinkTopologyMatrix_edited.append([port_address, port_value, speed_link, portNameEnum])
                    LinkTopologyMatrix_edited.append([devNUM, portNameEnum, portNUM, speed_link])
                    #LinkTopologyMatrix_edited.append([top])
                    notFoundFlag = False

    print(LinkTopologyMatrix_edited)
    # print(PortNamesMatrix)

    # link_id = []
    # devices = base_ONOS.readDevices (ctrl)
    # for dev in devices:
    #     devNum = str(devices[dev][0])
    #     ports = base_ONOS.readPorts(devNum, ctrl)
    #     for port in ports:
    #         portNum = str(ports[port][1])
    #         portName = str(ports[port][3]["portName"])
    #         if portNum != 'local' and len(portName) > 7:
                
    #             if int(portName[len(portName)-1]) > 1:
    #                 for edge in edgesInfo:
    #                     try:
    #                         edgePortFWD = 'c.'+edgesInfo[edge]['id']+'-'+edgesInfo[edge]['id']
    #                         portSpeed = edgesInfo[edge]['speed']
    #                         # print(portName)
    #                         if str(edgePortFWD) == str(portName[:-2]):
    #                             link_id.append(edgesInfo[edge]['id'])
                            
                            
    #                     except:
    #                         pass
                    
                    # print(set(link_id))

    # print(link_id)
    # for edge in link_id:
    #     print(edgesInfo[edge])