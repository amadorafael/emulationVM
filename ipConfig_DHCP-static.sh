#!/bin/bash
# Demonstrate how read actually works
echo 'IP configuration:'
echo 'Please type 1 for DHCP or type 2 for Static'
read ipType

if [[ $ipType == 1 ]] ; then
    config=$(sed '37q;d' /home/vm/emu/deploy_system.sh)
    if [[ "$config" == 'sudo dhclient enp0s3' ]] ; then
        echo "DHCP is already enabled"
        sleep 2
    else
        echo ${config}
        var=$(echo "$config" | sed 's/\//\\\//g')
        sed -i "/${var}/c sudo dhclient enp0s3" /home/vm/emu/deploy_system.sh
        echo "DHCP is now enabled"
        sleep 2
    fi
else
	echo "Please enter the IP Address in the format 'IPAdress/Mask - ex: 172.16.0.10/24'"
    read ipExt
    config=$(sed '37q;d' /home/vm/emu/deploy_system.sh)
    var=$(echo "$config" | sed 's/\//\\\//g')
    sed -i "/${var}/c sudo ifconfig enp0s3 ${ipExt} up" /home/vm/emu/deploy_system.sh
    echo "Static IP Address ${ipExt} is now enabled"
    sleep 2
fi