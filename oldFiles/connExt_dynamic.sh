#!/bin/bash

#####################################
# Rafael Amado (rgamado@gmail.com)
# Synchromedia Laboratory - ETS
# 2020-06-26
####################################

appSW=$1
devSW=$2

echo $appSW
echo $devSW


# # This one works:
# sudo ovs-vsctl add-br sw09
# sudo ovs-vsctl add-port sw09 enp0s3

# ext_ip=$(ifconfig enp0s3 | grep "inet " | awk '{print $2}')
# if [ -z "$ext_ip" ]
# then
# 	ext_ip=$(ifconfig sw09 | grep "inet " | awk '{print $2}')
# 	echo " ** sw09 already has IP address** "
# else
# 	echo " ** extracting IP address from enp0s3 ** "
# fi

# sudo ifconfig enp0s3 0.0.0.0
# sudo ifconfig sw09 "${ext_ip}/24" up
# #sudo ifconfig sw09 172.24.20.78/24 up
# sudo route add default gw "${ext_ip:0:10}1" dev sw09
# #sudo route add default gw 172.24.20.1 dev sw09

# sudo ip link add c.sw09 type veth peer name c.sw07
# sudo ovs-vsctl add-port sw07 c.sw07
# sudo ovs-vsctl add-port sw09 c.sw09
# sudo ifconfig c.sw07 up
# sudo ifconfig c.sw09 up

# sudo ovs-vsctl add-br sw08
# sudo ovs-vsctl add-port sw08 enp0s8
# #sudo ifconfig sw08 10.0.0.10/24 up
# sudo ifconfig sw08 up

# sudo ip link add c.sw08 type veth peer name c.sw06
# sudo ovs-vsctl add-port sw06 c.sw06
# sudo ovs-vsctl add-port sw08 c.sw08
# sudo ifconfig c.sw06 up
# sudo ifconfig c.sw08 up


