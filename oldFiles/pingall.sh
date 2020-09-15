#!/bin/bash

export PATH="$PATH:bin:onos/bin"

echo "PINGALL to rediscover hosts"

ip=$(docker container inspect onos | grep \"IPAddress | cut -d: -f2 | sort -u | tr -d '", ')

echo " --- ACTIVATE FWD --- "
onos $ip app activate org.onosproject.fwd

# Connectivity Test
echo "ping app1 - iot1"
sudo ip netns exec Host-00 ping -c4 10.0.40.40
echo "ping app2 - iot2"
sudo ip netns exec Host-01 ping -c4 10.0.50.50
echo "ping app3 - iot3"
sudo ip netns exec Host-02 ping -c4 10.0.60.60

echo " --- DEACTIVATE FWD --- "
onos $ip app deactivate org.onosproject.fwd