#!/bin/bash

##################################
# Rafael George Amado - ETS
# Created: 2020-09-14
##################################
# deploy_system.sh

# Clean ONOS Devices
python3 /home/vm/emu/cleanONOSdevs.py

# --- Grab topo from OVS Generator ---
docker exec ovs-gen-tuan /bin/sh -c "cat ovs-topo.sh" > ovs-mesh_generated.sh
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

# ------------------- Deploy topology ----------------
if ! sudo rm /var/lock/ovs-mesh.lock ; then
     echo 'no ovs-mesh.lock found'
else
     sudo rm /var/lock/ovs-mesh.lock
     echo 'unlocked ovs-mesh.lock'
fi 2>/dev/null
# rm /var/lock/ovs-mesh.lock
sudo bash ovs-mesh_generated.sh  > ovs-mesh_generated.log 2>&1 &
# # ---------------------------------------------------

echo '5 seconds to create the topology'
sleep 5

echo 'Listing available ports'
for br in $(sudo ovs-vsctl list-br) ; do
    for port in $(sudo ovs-vsctl list-ports $br) ; do
        if [ $br != 'extbr' ] && [ $br != 'extbl' ] ; then
            echo $port
        fi
    done
done

# ---------------- Detect Edges ------------------------
for br in $(sudo ovs-vsctl list-br) ; do
    for port in $(sudo ovs-vsctl list-ports $br) ; do
        # Connect left edge
        if [[ $(echo $port | grep host |  cut -d "." -f2 | cut -d "-" -f1) == 'host00' ]] ; then
            swNameR=$(echo $port | grep host |  cut -d "." -f2 | cut -d "-" -f2)
            # echo c.$swNameR
            sudo ip link add c.extbr type veth peer name c.$swNameR
            sudo ovs-vsctl add-port $swNameR c.$swNameR
            sudo ovs-vsctl add-port extbr c.extbr
            sudo ifconfig c.$swNameR up
            sudo ifconfig c.extbr up
        fi
        # Connect right edge
        if [[ $(echo $port | grep host |  cut -d "." -f2 | cut -d "-" -f1) == 'host01' ]] ; then
            swNameL=$(echo $port | grep host |  cut -d "." -f2 | cut -d "-" -f2)
            # echo c.$swNameL
            sudo ip link add c.extbl type veth peer name c.$swNameL
            sudo ovs-vsctl add-port $swNameL c.$swNameL
            sudo ovs-vsctl add-port extbl c.extbl
            sudo ifconfig c.$swNameL up
            sudo ifconfig c.extbl up
        fi
    done
done
# ---------------------------------------------------------------------------------------------------
# Link speeds
# --------------------- INGRESS POLICIES -------------------------------------------------------------
# At the moment, all ports are set to 100Mbps
#----------------------------------------------------------------------------------------------------
for br in $(sudo ovs-vsctl list-br) ; do
    for port in $(sudo ovs-vsctl list-ports $br) ; do
        # echo $port
        sudo ovs-vsctl set interface $port ingress_policing_rate=100000
        sudo ovs-vsctl set interface $port ingress_policing_burst=80000
    done
done
# ---------------------------------------------------------------------------------------------------

echo '3 seconds to set all ingress policies'
sleep 3

# Send netcfg to ONOS
python3 /home/vm/emu/create_netcfg.py





