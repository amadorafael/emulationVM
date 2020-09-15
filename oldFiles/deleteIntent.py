#!/usr/bin/python3

###################################################
# Rafael George Amado - ETS
# 2020-05-11
###################################################

# imports
import json, requests, sys, time, os
import pce
import base_ONOS

len(sys.argv)
key1 = sys.argv[1]
key2 = sys.argv[2]

ctrl = 'http://172.17.0.2:8181/onos/v1/'


if __name__ == '__main__':

    del_int = base_ONOS.deleteIntent (ctrl, key1, key2)