#!/bin/bash

# --- Clean old Topology ---
# Cleaning links
for i in $(sudo ip link list | grep sw |  cut -d "@" -f1 | awk '{print $2}') ; do
    sudo ip link del dev $i
done
# Cleaning bridges/ports
for br in $(sudo ovs-vsctl list-br) ; do
    for port in $(sudo ovs-vsctl list-ports $br) ; do
        if [ $br != 'extbr' ] && [ $br != 'extbl' ] ; then
            sudo ip link del $port
            sudo ovs-vsctl --if-exists del-port $br $port
            # echo 'Deleting port' ${port}
        fi
    done
    sudo ovs-vsctl --if-exists del-br $br
    # echo 'Deleting bridge' ${br}
done
# DHCP configuration (you might change it to static)
sudo dhclient enp0s3
sudo ovs-vsctl add-br extbr
sudo ovs-vsctl add-port extbr enp0s3

ext_ip=$(ifconfig enp0s3 | grep "inet " | awk '{print $2}')
if [ -z "$ext_ip" ]
then
	ext_ip=$(ifconfig extbr | grep "inet " | awk '{print $2}')
	echo " ** extbr already has IP address** "
else
	echo " ** extracting IP address from enp0s3 ** "
fi

# First external interface
sudo ifconfig enp0s3 0.0.0.0
sudo ifconfig extbr "${ext_ip}/24" up
sudo route add default gw "${ext_ip:0:10}1" dev extbr

# Second external interface
sudo ovs-vsctl add-br extbl
sudo ovs-vsctl add-port extbl enp0s8
sudo ifconfig extbl up