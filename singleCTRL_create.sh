#!/bin/bash
export PATH="$PATH:bin:onos/bin"

####################################
# Rafael Amado (rgamado@gmail.com)
# Synchromedia Laboratory - ETS
# 2020-04-28
####################################


SSH_KEY=$(cut -d\  -f2 ~/.ssh/id_rsa.pub)

# Destroy the ONOS cluster running as docker images
echo "Destroying onos..."
docker stop onos

docker container prune --force

# Create ONOS cluster using ONOS docker image
# ONOS_IMAGE=onosproject/onos:1.15.0
# ONOS_IMAGE=onosproject/onos:2.0.0
ONOS_IMAGE=onosproject/onos:latest



docker run -p 127.0.0.1:6653:6653 -p 8181:8181 -dit --name onos --hostname onos --restart=unless-stopped $ONOS_IMAGE
docker exec -it onos bin/onos-user-key vm $SSH_KEY  >/dev/null 2>&1
docker exec -it onos bin/onos-user-password onos rocks >/dev/null 2>&1

function waitForStart {
    sleep 5
    ip=$(docker container inspect onos | grep \"IPAddress | cut -d: -f2 | sort -u | tr -d '", ')
    for t in {1..60}; do
        curl --fail -sS http://$ip:8181/onos/v1/applications --user onos:rocks 1>/dev/null 2>&1 && break;
        sleep 1;
    done
}

waitForStart

# Installing extra
echo "Activating OpenFlow, ProxyARP  and IFWD applications..."

ip=$(docker container inspect onos | grep \"IPAddress | cut -d: -f2 | sort -u | tr -d '", ')
echo "OPENFLOW"
/home/vm/emu/onos/bin/onos $ip app activate org.onosproject.openflow

echo "FWD"
/home/vm/emu/onos/bin/onos $ip app activate org.onosproject.fwd

echo "ARP"
/home/vm/emu/onos/bin/onos $ip app activate org.onosproject.proxyarp 

echo "LAYOUT"
/home/vm/emu/onos/bin/onos $ip app activate org.onosproject.layout

echo "PATH PAINTER"
/home/vm/emu/onos/bin/onos $ip app activate org.onosproject.pathpainter

# Network Setup 
# Policies, Host IP addresses, etc
# echo " --- NETWORK SETUP --- "
# sudo bash network_setup.sh 

#echo " --- DEACTIVATE FWD --- "
#onos $ip app deactivate org.onosproject.fwd

echo "Remove old ssh key for 'karaf' "
ssh-keygen -f "/home/vm/.ssh/known_hosts" -R "[${ip}]:8101"

# echo "Starting the NodeJS server"
# /usr/bin/nodejs app.js
