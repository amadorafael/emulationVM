import json, requests, sys, time, os
from datetime import datetime
import pce
import base_ONOS

ctrl = 'http://172.17.0.3:8181/onos/v1/'

devices = base_ONOS.readDevices (ctrl)
for dev in devices:
    # print(devices[dev])
    status = str(devices[dev][2])
    devNum = str(devices[dev][0])
    # print(status)    
    try:
        status.index('disconnected')
    except ValueError:
        # print('Transport Switch')
        print(status)
    else:
        print('Deleting device: ', devNum)
        base_ONOS.deleteDevice ( devNum, ctrl )