#!/usr/bin/python3

##################################
# Rafael Amado (rgamado@gmail.com)
# Synchromedia Laboratory - ETS
# 2020-04-28
##################################

import json, requests, sys, time, os
import base_ONOS

lowPath = ['sw06', 'sw04', 'sw05', 'sw07']
highPath = ['sw06', 'sw01', 'sw02', 'sw03', 'sw07']

# lowPath = ['sw06', 'sw04', 'sw02', 'sw05', 'sw03', 'sw07']

ctrl = 'http://localhost:8181/onos/v1/'


def readDevices ( ctrl ):
	deviceList = {}
	response  = requests.get(ctrl+'devices/', auth=('onos', 'rocks'))
	response.raise_for_status()
	data_loaded = json.loads(response.text)
	for num, data in enumerate(data_loaded['devices']):
		deviceList[num] = (data['id'],data['type'])
	return deviceList

def linkLoad( Path, BW ):
    devices = {}
    linksPath = {"path":[]}
    for num, dev in enumerate(Path):
        devices[num] = dev
        # print(len(devices))
    for num in devices:
        if num < len(devices)-1:
            sw = 'of:00000000000000'+str(devices[num][2:4])
            links = base_ONOS.readLinks (ctrl)
            srcPort = assignPorts(devices[num], devices[num+1])
            for i in links:
                if (links[i][0]["device"] == sw) and (links[i][0]["port"] == srcPort):
                    srcDev = links[i][0]["device"]
                    srcPort = links[i][0]["port"]
                    dstDev = links[i][1]["device"]
                    dstPort = links[i][1]["port"]
            jsonPath = {"srcDev": str(srcDev), "srcPort": str(srcPort), "dstDev": str(dstDev), "dstPort": str(dstPort), "BW": str(BW) } 
            linksPath['path'].append(jsonPath)
    write_json(linksPath)
    return linksPath

# function to add to JSON 
def write_json(data, filename='link_loads.json'): 
    with open(filename,'w') as f: 
        json.dump(data, f, indent=4) 

def assignPorts (dev1c, dev2c):
    dev1 = dev1c[2:4]
    dev2 = dev2c[2:4]
    devices = base_ONOS.readDevices (ctrl)
    for dev in devices:
        devNum = str(devices[dev][0])
        # print(devNum)
        ports = base_ONOS.readPorts(devNum, ctrl)
        if devNum[17:19] == dev1:
            for port in ports:
                portNum = str(ports[port][1])
                portName = str(ports[port][3]["portName"])    
                nomePorta = 'c.'+dev1c+'-'+dev2c+'.1'
                if portName == nomePorta:    
                    assignedPort = portNum
                    return assignedPort
 
def get_paths(BW):

    if BW <= 50:
        path = lowPath
    else:
        path = highPath

    path_links = linkLoad(path,BW)
    return path

# # def main(BW, srcIP, dstIP):

    

# if __name__ == '__main__':

#     path = get_paths(BW)
#     x = linkLoad (path, BW)
#     print(len(x))
#     y = '{"path": ['+str(x)+']}'
#     print(y)
#     write_json(x)
