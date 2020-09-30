
#!/usr/bin/python3

###################################################
# Rafael Amado (rgamado@gmail.com)
# Synchromedia Laboratory - ETS
# Created: 2020-04-28
# Modified: 2020-09-14
###################################################
# Base functions used in api_v1.py and pce.py
###################################################


# imports
import json, requests, sys, time, os

def readFlows (ctrl):
    flows = {}
    response  = requests.get(ctrl+'flows/', auth=('onos', 'rocks'))
    data_loaded = json.loads(response.text)
    for data in data_loaded['flows']:
        flows[data["id"]] = [data["priority"], data["state"], data["deviceId"]]
    return flows

def installFlowRules( device, rule, ctrl ):
	headers = {'Content-Type': 'application/json',}
	installRule  = requests.post(ctrl+'flows/%s' % device, headers=headers, data=json.dumps(rule), auth=('onos', 'rocks'))
	print(installRule.text)
	headPost = installRule.headers['Location']
	flowInstalled = headPost.split('/')[6:]
	return flowInstalled

def deleteFlowRules( rule, ctrl ):
    requests.delete(ctrl+'flows/%s' % rule, auth=('onos', 'rocks'))

def readLinks ( ctrl ):
	linkLive = {}
	response  = requests.get(ctrl+'links/', auth=('onos', 'rocks'))
	data_loaded = json.loads(response.text)
	for num, j in enumerate(data_loaded['links']):
		linkLive[num] = (j['src'], j['dst'], j['state'])
	return linkLive

def readPath ( edgeSwitches, ctrl ):
	pathLive = {}
	edgess = str(edgeSwitches[app][0])+'/'+str(edgeSwitches[iot][0])
	response  = requests.get(ctrl+'paths/%s' % edgess, auth=('onos', 'rocks'))
	data_loaded = json.loads(response.text)
	for num1, data in enumerate(data_loaded['paths']):
		for num2, line in enumerate(data['links']):
			pathLive[num2] = (line['src']['device'],line['src']['port'], line['dst']['device'], line['dst']['port'], line['state'])
	return pathLive

def readHosts ( ctrl ):
	edge = {}
	hostIP = {}
	response  = requests.get(ctrl+'hosts/', auth=('onos', 'rocks'))
	response.raise_for_status()
	data_loaded = json.loads(response.text)
	for data in data_loaded['hosts']:
		for location in data['locations']:
			try:
				edge[data['id']].append(location['elementId'],location['port'])
			except KeyError:
				edge[data['id']] = [location['elementId'],location['port']]
	return edge

def readIPs ( ctrl ):
	hostIP = {}
	macEdge = {}
	response  = requests.get(ctrl+'hosts/', auth=('onos', 'rocks'))
	response.raise_for_status()
	data_loaded = json.loads(response.text)
	for data in data_loaded['hosts']:
		hostIP[data['id']] = [str(data['ipAddresses'][0]), str(data['mac'])]
	return hostIP

def readHostIPport (ctrl,ipAdd):
    hosts = readHosts(ctrl)
    ips = readIPs(ctrl)
    host = {}
    hostInfo = {}
    for i in hosts:
        host[i] = [ips[i], hosts[i]]
        hostInfo[i] = [str(host[i][0][0]), str(host[i][1][0]), str(host[i][1][1]), host[i][0][1] ]
    for i in hostInfo:
        if hostInfo[i][0] == str(ipAdd):
            device = hostInfo[i][1]
            port = hostInfo[i][2]
            mac = hostInfo[i][3]
            return device, port, mac


def readPorts ( device, ctrl ):
	devPorts = {}
	response  = requests.get(ctrl+'devices/%s/ports' % device, auth=('onos', 'rocks'))
	response.raise_for_status()
	data_loaded = json.loads(response.text)
	for num, data in enumerate(data_loaded['ports']):
		try:
			devPorts[num] = [data['element'], data['port'], data['isEnabled'], data['annotations']]
		except KeyError:
			print('No annotatios found')
			devPorts[num] = [data['element'], data['port'], data['isEnabled']]
	return devPorts

def readDevices ( ctrl ):
	deviceList = {}
	response  = requests.get(ctrl+'devices/', auth=('onos', 'rocks'))
	response.raise_for_status()
	data_loaded = json.loads(response.text)
	for num, data in enumerate(data_loaded['devices']):
		deviceList[num] = (data['id'],data['type'],data['humanReadableLastUpdate'])
	return deviceList

def deleteDevice ( device, ctrl ):
	response  = requests.delete(ctrl+'devices/%s' % device, auth=('onos', 'rocks'))
	response.raise_for_status()
	print(response)

def readIntents ( ctrl ):
	intentList = {}
	response  = requests.get(ctrl+'intents/', auth=('onos', 'rocks'))
	response.raise_for_status()
	data_loaded = json.loads(response.text)
	for num, data in enumerate(data_loaded['intents']):
		intentList[num] = (data['key'],data['appId'])
		# print(intentList)
		key=str(intentList[num][0])
		appId = str(intentList[num][1])
		# print(ctrl+'intents/%s/%s' % appId, key)
		response  = requests.get(ctrl+'intents/%s/%s' % (appId, key), auth=('onos', 'rocks'))
		response.raise_for_status()
		data_loaded = json.loads(response.text)
		# print(data_loaded)
	return intentList


def intentDetails (ctrl):
	intentList = {}
	response  = requests.get(ctrl+'intents/', auth=('onos', 'rocks'))
	response.raise_for_status()
	data_loaded = json.loads(response.text)
	for num, data in enumerate(data_loaded['intents']):
		# print(data)
		intentList[num] = (data['key'])
		key=str(intentList[num])
		# print(key)
		response2 = requests.get(ctrl+'intents/org.onosproject.cli/%s' % key, auth=('onos', 'rocks'))
		response2.raise_for_status()
		data_loaded2 = json.loads(response2.text)
		# print(data_loaded2)
		print(data_loaded2['selector']['criteria'][1], data_loaded2['selector']['criteria'][2], data_loaded2['constraints'][0])
		print('---------')
		response3 = requests.get(ctrl+'intents/installables/org.onosproject.cli/%s' % key, auth=('onos', 'rocks'))
		response3.raise_for_status()
		data_loaded3 = json.loads(response3.text)
		# print(data_loaded3)
		for rule in data_loaded3['installables']:
			print(rule['key'])
			# print(rule['resources'])
			for resource in rule['resources']:
				print(resource['src'], resource['dst'], resource['annotations'])
		# print(data_loaded3['installables'])
		print('==========')
	return intentList

def deleteIntent (ctrl, key1, key2):
	requests.delete(ctrl+'intents/org.onosproject.cli/%s' % key1, auth=('onos', 'rocks'))
	requests.delete(ctrl+'intents/org.onosproject.cli/%s' % key1, auth=('onos', 'rocks'))


def intentPOST (ctrl, intent):
	headers = {'Content-Type': 'application/json',}
	intent_install  = requests.post(ctrl+'intents/', headers=headers, data=json.dumps(intent), auth=('onos', 'rocks'))
	intent_install.raise_for_status()
	# print(intent_install.headers)


def configPOST (ctrl, dir):
	# files = []
	for file in os.listdir(dir):
		if file.endswith('.json'):
			with open( os.path.join( dir, file ) ) as fd:
				config = json.load(fd)
	headers = {'Content-Type': 'application/json',}
	config_install  = requests.post(ctrl+'network/configuration/', headers=headers, data=json.dumps(config), auth=('onos', 'rocks'))
	config_install.raise_for_status()


def config_netcfg_POST (ctrl, config):
	# config = json.dumps(rule)
	# print('--- config check ---')

	# print(json.dumps(config))

	# print('--------------------')
	headers = {'Content-Type': 'application/json',}
	config_install  = requests.post(ctrl+'network/configuration/', headers=headers, data=json.dumps(config), auth=('onos', 'rocks'))
	config_install.raise_for_status()