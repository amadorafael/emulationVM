#!/usr/bin/python3

###################################################
# Rafael George Amado - ETS
# 2020-05-11
###################################################

# imports
import json, requests, sys, time, os
import pce
import base_ONOS

ctrl = 'http://172.17.0.2:8181/onos/v1/'


if __name__ == '__main__':

    inst_int = base_ONOS.intentDetails (ctrl)
    # print(inst_int)


    # flows = base_ONOS.readFlows(ctrl)
    # for flow in flows:
    #     if flows[flow][0] == 50001:
    #         print(flows[flow][2])
    # # print(flows)