#!/bin/bash

##################################
# Rafael Amado (rgamado@gmail.com)
# Synchromedia Laboratory - ETS
# Created: 2020-04-28
##################################

##### Configure Hosts IP Addresses ####
echo "configuring hosts IP addresses"
sudo ip netns exec Host-00 ifconfig c.sw06-host00.1 10.0.10.10 netmask 255.255.255.0
sudo ip netns exec Host-00 ifconfig c.sw06-host00.1 hw ether 10:10:10:10:10:10
sudo ip netns exec Host-00 ip route add default dev c.sw06-host00.1 #proto kernel scope link src 10.0.10.10

sudo ip netns exec Host-01 ifconfig c.sw06-host01.1 10.0.20.20 netmask 255.255.255.0 
sudo ip netns exec Host-01 ifconfig c.sw06-host01.1 hw ether 20:20:20:20:20:20
sudo ip netns exec Host-01 ip route add default dev c.sw06-host01.1 #proto kernel scope link src 10.0.20.20

sudo ip netns exec Host-02 ifconfig c.sw06-host02.1 10.0.30.30 netmask 255.255.255.0 
sudo ip netns exec Host-02 ifconfig c.sw06-host02.1 hw ether 30:30:30:30:30:30
sudo ip netns exec Host-02 ip route add default dev c.sw06-host02.1 #proto kernel scope link src 10.0.30.30

sudo ip netns exec Host-03 ifconfig c.sw07-host03.1 10.0.40.40 netmask 255.255.255.0 
sudo ip netns exec Host-03 ifconfig c.sw07-host03.1 hw ether 40:40:40:40:40:40
sudo ip netns exec Host-03 ip route add default dev c.sw07-host03.1 #proto kernel scope link src 10.0.40.40

sudo ip netns exec Host-04 ifconfig c.sw07-host04.1 10.0.50.50 netmask 255.255.255.0 
sudo ip netns exec Host-04 ifconfig c.sw07-host04.1 hw ether 50:50:50:50:50:50
sudo ip netns exec Host-04 ip route add default dev c.sw07-host04.1 #proto kernel scope link src 10.0.50.50

sudo ip netns exec Host-05 ifconfig c.sw07-host05.1 10.0.60.60 netmask 255.255.255.0 
sudo ip netns exec Host-05 ifconfig c.sw07-host05.1 hw ether 60:60:60:60:60:60
sudo ip netns exec Host-05 ip route add default dev c.sw07-host05.1 #proto kernel scope link src 10.0.60.60

# Connectivity Test
echo "ping app1 - iot1"
sudo ip netns exec Host-00 ping -c4 10.0.40.40
echo "ping app2 - iot2"
sudo ip netns exec Host-01 ping -c4 10.0.50.50
echo "ping app3 - iot3"
sudo ip netns exec Host-02 ping -c4 10.0.60.60



# SINGLE NETWORK
# ##### Configure Hosts IP Addresses ####
# echo "configuring hosts IP addresses"
# sudo ip netns exec Host-00 ifconfig c.sw06-host00.1 10.0.0.1 netmask 255.255.255.0
# sudo ip netns exec Host-01 ifconfig c.sw06-host01.1 10.0.0.2 netmask 255.255.255.0 
# sudo ip netns exec Host-02 ifconfig c.sw06-host02.1 10.0.0.3 netmask 255.255.255.0 
# sudo ip netns exec Host-03 ifconfig c.sw07-host03.1 10.0.0.11 netmask 255.255.255.0 
# sudo ip netns exec Host-04 ifconfig c.sw07-host04.1 10.0.0.12 netmask 255.255.255.0 
# sudo ip netns exec Host-05 ifconfig c.sw07-host05.1 10.0.0.13 netmask 255.255.255.0 

# # Connectivity Test
# echo "ping app1 - iot1"
# sudo ip netns exec Host-00 ping -c4 10.0.0.11
# echo "ping app2 - iot2"
# sudo ip netns exec Host-01 ping -c4 10.0.0.12
# echo "ping app3 - iot3"
# sudo ip netns exec Host-02 ping -c4 10.0.0.13

# Install default rules
# These are lowPath (sw06-sw04-sw05-sw07) and highPath (sw06-sw01-sw02-sw03-sw07) with priority 40001 just for start and ping all
echo "NO BASIC FLOWS INSTALLED"
# python basic_Flows_install.py

echo "Posting Link BW, Port Speed and BW to ONOS"
curl -X POST -H "content-type:application/json"  http://172.17.0.3:8181/onos/v1/network/configuration -d @links_ports_CONFIG.json --user onos:rocks

################ INGRESS POLICIES ###############

echo "applying ingress policies"
# Limit to 100Mbps

ovs-vsctl set interface c.sw01-sw02.1 ingress_policing_rate=100000
ovs-vsctl set interface c.sw01-sw02.1 ingress_policing_burst=80000
ovs-vsctl set interface c.sw02-sw01.1 ingress_policing_rate=100000
ovs-vsctl set interface c.sw02-sw01.1 ingress_policing_burst=80000

ovs-vsctl set interface c.sw02-sw03.1 ingress_policing_rate=100000
ovs-vsctl set interface c.sw02-sw03.1 ingress_policing_burst=80000
ovs-vsctl set interface c.sw03-sw02.1 ingress_policing_rate=100000
ovs-vsctl set interface c.sw03-sw02.1 ingress_policing_burst=80000

# Limit to 50Mbps
ovs-vsctl set interface c.sw01-sw04.1 ingress_policing_rate=50000
ovs-vsctl set interface c.sw01-sw04.1 ingress_policing_burst=8000
ovs-vsctl set interface c.sw04-sw01.1 ingress_policing_rate=50000
ovs-vsctl set interface c.sw04-sw01.1 ingress_policing_burst=8000

ovs-vsctl set interface c.sw02-sw04.1 ingress_policing_rate=50000
ovs-vsctl set interface c.sw02-sw04.1 ingress_policing_burst=8000
ovs-vsctl set interface c.sw04-sw02.1 ingress_policing_rate=50000
ovs-vsctl set interface c.sw04-sw02.1 ingress_policing_burst=8000

ovs-vsctl set interface c.sw02-sw05.1 ingress_policing_rate=50000
ovs-vsctl set interface c.sw02-sw05.1 ingress_policing_burst=8000
ovs-vsctl set interface c.sw05-sw02.1 ingress_policing_rate=50000
ovs-vsctl set interface c.sw05-sw02.1 ingress_policing_burst=8000

ovs-vsctl set interface c.sw05-sw04.1 ingress_policing_rate=50000
ovs-vsctl set interface c.sw05-sw04.1 ingress_policing_burst=8000
ovs-vsctl set interface c.sw04-sw05.1 ingress_policing_rate=50000
ovs-vsctl set interface c.sw04-sw05.1 ingress_policing_burst=8000

ovs-vsctl set interface c.sw03-sw05.1 ingress_policing_rate=50000
ovs-vsctl set interface c.sw03-sw05.1 ingress_policing_burst=8000
ovs-vsctl set interface c.sw05-sw03.1 ingress_policing_rate=50000
ovs-vsctl set interface c.sw05-sw03.1 ingress_policing_burst=8000

# Edges
ovs-vsctl set interface c.sw06-sw04.1 ingress_policing_rate=100000
ovs-vsctl set interface c.sw06-sw04.1 ingress_policing_burst=80000
ovs-vsctl set interface c.sw04-sw06.1 ingress_policing_rate=100000
ovs-vsctl set interface c.sw04-sw06.1 ingress_policing_burst=80000

ovs-vsctl set interface c.sw01-sw06.1 ingress_policing_rate=100000
ovs-vsctl set interface c.sw01-sw06.1 ingress_policing_burst=80000
ovs-vsctl set interface c.sw06-sw01.1 ingress_policing_rate=100000
ovs-vsctl set interface c.sw06-sw01.1 ingress_policing_burst=80000

ovs-vsctl set interface c.sw07-sw03.1 ingress_policing_rate=100000
ovs-vsctl set interface c.sw07-sw03.1 ingress_policing_burst=80000
ovs-vsctl set interface c.sw03-sw07.1 ingress_policing_rate=100000
ovs-vsctl set interface c.sw03-sw07.1 ingress_policing_burst=80000

ovs-vsctl set interface c.sw07-sw05.1 ingress_policing_rate=100000
ovs-vsctl set interface c.sw07-sw05.1 ingress_policing_burst=80000
ovs-vsctl set interface c.sw05-sw07.1 ingress_policing_rate=100000
ovs-vsctl set interface c.sw05-sw07.1 ingress_policing_burst=80000


# # Deactivate ONOS Reactive Forwarding 
# export PATH="$PATH:bin:onos/bin"
# echo "DEACTIVATE REACTIVE FORWADING"
# SSH_KEY=$(cut -d\  -f2 /home/vm/.ssh/id_rsa.pub)
# ip=$(docker container inspect onos | grep \"IPAddress | cut -d: -f2 | sort -u | tr -d '", ')
# echo "FWD"
# /home/vm/onos/bin/onos $ip app activate org.onosproject.fwd
