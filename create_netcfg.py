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
            print(portName, portNum)
            if portNum == 'local': 
                # ---- config Device Names ONOS GUI ---- #
                nameConfig = {"devices": {devNum: { "basic": { "name": portName  } } }}
                print('Switch Name: '+portName)
                base_ONOS.config_netcfg_POST (ctrl, nameConfig)
            
    # ---------------- Port Speeds Configuration | netcfg file POST ------------------

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


    print(edgesInfo)
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
                                print('SOURCE')
                                print(portConfig)
                                base_ONOS.config_netcfg_POST (ctrl, portConfig)

                                ## Ingress Policies config
                                ovs(portName,portSpeed)

                                linksONOS = base_ONOS.readLinks(ctrl)
                                for link in linksONOS:
                                    srcPort = linksONOS[link][0]['port']
                                    srcDevice = linksONOS[link][0]['device']
                                    if str(devices[dev][0]) == str(srcDevice) and str(portNum) == str(srcPort):
                                        dstDev = linksONOS[link][1]['device']
                                        dstPort = linksONOS[link][1]['port']
                                        portConfig = {"devices": {str(dstDev): { "ports": { str(dstPort): { "number": dstPort, "speed": portSpeed } } } },"ports": {str(dstDev)+"/"+str(dstPort): {"bandwidthCapacity": { "capacityMbps": portSpeed } } }} # MUST ADAPT TO READ FILE WITH LINKS FROM OVS-MESH
                                        print('DESTINATION')
                                        print(portConfig)
                                        base_ONOS.config_netcfg_POST (ctrl, portConfig)

                                        portsDst = base_ONOS.readPorts(dstDev, ctrl)
                                        for port in portsDst:
                                            portNumDst = str(portsDst[port][1])
                                            portNameDst = str(portsDst[port][3]["portName"])
                                            if portNumDst == dstPort:
                                                # print(portNameDst)

                                                ## Ingress Policies config
                                                ovs(portNameDst,portSpeed)

                        except KeyError:
                            pass      
                else:
                    print('More than one interface in this port')
                    # pass
                    # numInt = int(portName[len(portName)-1])
                    # for interf in range(1,numInt+1):
                    #     for edge in edgesInfo:
                    #         try:
                    #         # Check portNames vs Edges Info - one direction
                    #         edgePortsFWD = 'c.'+edgesInfo[edge]['from']+'-'+edgesInfo[edge]['to']
                    #         portSpeed = edgesInfo[edge]['speed']
                    #         # print('CheckPoint FWD')
                    #         # print(edgePortsFWD, portName[:-2])
                    #         if str(edgePortsFWD) == str(portName[:-2]):
                    #             portConfig = {"devices": {str(devNum): { "ports": { str(portNum): { "number": portNum, "speed": portSpeed } } } },"ports": {str(devNum)+"/"+str(portNum): {"bandwidthCapacity": { "capacityMbps": portSpeed } } }} # MUST ADAPT TO READ FILE WITH LINKS FROM OVS-MESH
                    #             print('SOURCE')
                    #             print(portConfig)
                    #             base_ONOS.config_netcfg_POST (ctrl, portConfig)

                    #             ## Ingress Policies config
                    #             ovs(portName,portSpeed)

                    #             linksONOS = base_ONOS.readLinks(ctrl)
                    #             for link in linksONOS:
                    #                 srcPort = linksONOS[link][0]['port']
                    #                 srcDevice = linksONOS[link][0]['device']
                    #                 if str(devices[dev][0]) == str(srcDevice) and str(portNum) == str(srcPort):
                    #                     dstDev = linksONOS[link][1]['device']
                    #                     dstPort = linksONOS[link][1]['port']
                    #                     portConfig = {"devices": {str(dstDev): { "ports": { str(dstPort): { "number": dstPort, "speed": portSpeed } } } },"ports": {str(dstDev)+"/"+str(dstPort): {"bandwidthCapacity": { "capacityMbps": portSpeed } } }} # MUST ADAPT TO READ FILE WITH LINKS FROM OVS-MESH
                    #                     print('DESTINATION')
                    #                     print(portConfig)
                    #                     base_ONOS.config_netcfg_POST (ctrl, portConfig)

                    #                     portsDst = base_ONOS.readPorts(dstDev, ctrl)
                    #                     for port in portsDst:
                    #                         portNumDst = str(portsDst[port][1])
                    #                         portNameDst = str(portsDst[port][3]["portName"])
                    #                         if portNumDst == dstPort:
                    #                             # print(portNameDst)

                    #                             ## Ingress Policies config
                    #                             ovs(portNameDst,portSpeed)

