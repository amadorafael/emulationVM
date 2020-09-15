#!/bin/bash

DEFAULT_CONTROLLER=tcp:127.0.0.1:6653
DEFAULT_LISTEN=ptcp:6634
DEFAULT_OFv=OpenFlow13

echo -e '\n(Re-)creating OVS instances...'

ovs-vsctl -- --id=@sw create Controller 'target="tcp:127.0.0.1:6653"' max_backoff=1000 -- --id=@sw00-listen create Controller 'target="ptcp:6634"' max_backoff=1000 -- --if-exists del-br sw00 -- add-br sw00 -- set bridge sw00 'controller=[@sw,@sw00-listen]' other_config:datapath-id=0000000000000000 fail_mode=secure other-config:disable-in-band=true protocols=OpenFlow13

ovs-vsctl -- --id=@sw create Controller 'target="tcp:127.0.0.1:6653"' max_backoff=1000 -- --id=@sw01-listen create Controller 'target="ptcp:6634"' max_backoff=1000 -- --if-exists del-br sw01 -- add-br sw01 -- set bridge sw01 'controller=[@sw,@sw01-listen]' other_config:datapath-id=0000000000000001 fail_mode=secure other-config:disable-in-band=true protocols=OpenFlow13

ovs-vsctl -- --id=@sw create Controller 'target="tcp:127.0.0.1:6653"' max_backoff=1000 -- --id=@sw02-listen create Controller 'target="ptcp:6634"' max_backoff=1000 -- --if-exists del-br sw02 -- add-br sw02 -- set bridge sw02 'controller=[@sw,@sw02-listen]' other_config:datapath-id=0000000000000002 fail_mode=secure other-config:disable-in-band=true protocols=OpenFlow13

ovs-vsctl -- --id=@sw create Controller 'target="tcp:127.0.0.1:6653"' max_backoff=1000 -- --id=@sw03-listen create Controller 'target="ptcp:6634"' max_backoff=1000 -- --if-exists del-br sw03 -- add-br sw03 -- set bridge sw03 'controller=[@sw,@sw03-listen]' other_config:datapath-id=0000000000000003 fail_mode=secure other-config:disable-in-band=true protocols=OpenFlow13

ovs-vsctl -- --id=@sw create Controller 'target="tcp:127.0.0.1:6653"' max_backoff=1000 -- --id=@sw04-listen create Controller 'target="ptcp:6634"' max_backoff=1000 -- --if-exists del-br sw04 -- add-br sw04 -- set bridge sw04 'controller=[@sw,@sw04-listen]' other_config:datapath-id=0000000000000004 fail_mode=secure other-config:disable-in-band=true protocols=OpenFlow13

ovs-vsctl -- --id=@sw create Controller 'target="tcp:127.0.0.1:6653"' max_backoff=1000 -- --id=@sw05-listen create Controller 'target="ptcp:6634"' max_backoff=1000 -- --if-exists del-br sw05 -- add-br sw05 -- set bridge sw05 'controller=[@sw,@sw05-listen]' other_config:datapath-id=0000000000000005 fail_mode=secure other-config:disable-in-band=true protocols=OpenFlow13

ovs-vsctl -- --id=@sw create Controller 'target="tcp:127.0.0.1:6653"' max_backoff=1000 -- --id=@sw06-listen create Controller 'target="ptcp:6634"' max_backoff=1000 -- --if-exists del-br sw06 -- add-br sw06 -- set bridge sw06 'controller=[@sw,@sw06-listen]' other_config:datapath-id=0000000000000006 fail_mode=secure other-config:disable-in-band=true protocols=OpenFlow13

ovs-vsctl -- --id=@sw create Controller 'target="tcp:127.0.0.1:6653"' max_backoff=1000 -- --id=@sw07-listen create Controller 'target="ptcp:6634"' max_backoff=1000 -- --if-exists del-br sw07 -- add-br sw07 -- set bridge sw07 'controller=[@sw,@sw07-listen]' other_config:datapath-id=0000000000000007 fail_mode=secure other-config:disable-in-band=true protocols=OpenFlow13

ovs-vsctl list-br

echo -e '\nInstantiating virtual crossover cables...'

ip link add name c.sw02-sw01.1 type veth peer name c.sw01-sw02.1
ip link set c.sw02-sw01.1 up
ip link set c.sw01-sw02.1 up

ip link add name c.sw03-sw02.1 type veth peer name c.sw02-sw03.1
ip link set c.sw03-sw02.1 up
ip link set c.sw02-sw03.1 up

ip link add name c.sw04-sw01.1 type veth peer name c.sw01-sw04.1
ip link set c.sw04-sw01.1 up
ip link set c.sw01-sw04.1 up

ip link add name c.sw04-sw02.1 type veth peer name c.sw02-sw04.1
ip link set c.sw04-sw02.1 up
ip link set c.sw02-sw04.1 up

ip link add name c.sw05-sw02.1 type veth peer name c.sw02-sw05.1
ip link set c.sw05-sw02.1 up
ip link set c.sw02-sw05.1 up

ip link add name c.sw05-sw03.1 type veth peer name c.sw03-sw05.1
ip link set c.sw05-sw03.1 up
ip link set c.sw03-sw05.1 up

ip link add name c.sw05-sw04.1 type veth peer name c.sw04-sw05.1
ip link set c.sw05-sw04.1 up
ip link set c.sw04-sw05.1 up

ip link add name c.sw06-sw01.1 type veth peer name c.sw01-sw06.1
ip link set c.sw06-sw01.1 up
ip link set c.sw01-sw06.1 up

ip link add name c.sw06-sw04.1 type veth peer name c.sw04-sw06.1
ip link set c.sw06-sw04.1 up
ip link set c.sw04-sw06.1 up

ip link add name c.sw07-sw03.1 type veth peer name c.sw03-sw07.1
ip link set c.sw07-sw03.1 up
ip link set c.sw03-sw07.1 up

ip link add name c.sw07-sw05.1 type veth peer name c.sw05-sw07.1
ip link set c.sw07-sw05.1 up
ip link set c.sw05-sw07.1 up

echo -e '\nConnecting OVS instances to each other...\n'

ovs-vsctl add-port sw02 c.sw02-sw01.1 -- set Interface c.sw02-sw01.1 ofport_request=1
ovs-vsctl add-port sw01 c.sw01-sw02.1 -- set Interface c.sw01-sw02.1 ofport_request=1

ovs-vsctl add-port sw03 c.sw03-sw02.1 -- set Interface c.sw03-sw02.1 ofport_request=1
ovs-vsctl add-port sw02 c.sw02-sw03.1 -- set Interface c.sw02-sw03.1 ofport_request=1

ovs-vsctl add-port sw04 c.sw04-sw01.1 -- set Interface c.sw04-sw01.1 ofport_request=1
ovs-vsctl add-port sw01 c.sw01-sw04.1 -- set Interface c.sw01-sw04.1 ofport_request=1

ovs-vsctl add-port sw04 c.sw04-sw02.1 -- set Interface c.sw04-sw02.1 ofport_request=1
ovs-vsctl add-port sw02 c.sw02-sw04.1 -- set Interface c.sw02-sw04.1 ofport_request=1

ovs-vsctl add-port sw05 c.sw05-sw02.1 -- set Interface c.sw05-sw02.1 ofport_request=1
ovs-vsctl add-port sw02 c.sw02-sw05.1 -- set Interface c.sw02-sw05.1 ofport_request=1

ovs-vsctl add-port sw05 c.sw05-sw03.1 -- set Interface c.sw05-sw03.1 ofport_request=1
ovs-vsctl add-port sw03 c.sw03-sw05.1 -- set Interface c.sw03-sw05.1 ofport_request=1

ovs-vsctl add-port sw05 c.sw05-sw04.1 -- set Interface c.sw05-sw04.1 ofport_request=1
ovs-vsctl add-port sw04 c.sw04-sw05.1 -- set Interface c.sw04-sw05.1 ofport_request=1

ovs-vsctl add-port sw06 c.sw06-sw01.1 -- set Interface c.sw06-sw01.1 ofport_request=1
ovs-vsctl add-port sw01 c.sw01-sw06.1 -- set Interface c.sw01-sw06.1 ofport_request=1

ovs-vsctl add-port sw06 c.sw06-sw04.1 -- set Interface c.sw06-sw04.1 ofport_request=1
ovs-vsctl add-port sw04 c.sw04-sw06.1 -- set Interface c.sw04-sw06.1 ofport_request=1

ovs-vsctl add-port sw07 c.sw07-sw03.1 -- set Interface c.sw07-sw03.1 ofport_request=1
ovs-vsctl add-port sw03 c.sw03-sw07.1 -- set Interface c.sw03-sw07.1 ofport_request=1

ovs-vsctl add-port sw07 c.sw07-sw05.1 -- set Interface c.sw07-sw05.1 ofport_request=1
ovs-vsctl add-port sw05 c.sw05-sw07.1 -- set Interface c.sw05-sw07.1 ofport_request=1

echo -e '\nCreating hosts...\n'


ip netns add Host-00
ip netns add Host-01
ip netns add Host-02
ip netns add Host-03
ip netns add Host-04
ip netns add Host-05

echo -e '\nCreating and connecting virtual patch cables...\n'

ip link add c.sw06-host00.1 type veth peer name c.host00-sw06.1
ip link set c.sw06-host00.1 up
ip link set c.host00-sw06.1 up
ip link set c.sw06-host00.1 netns Host-00
ovs-vsctl add-port sw06 c.host00-sw06.1

ip link add c.sw06-host01.1 type veth peer name c.host01-sw06.1
ip link set c.sw06-host01.1 up
ip link set c.host01-sw06.1 up
ip link set c.sw06-host01.1 netns Host-01
ovs-vsctl add-port sw06 c.host01-sw06.1

ip link add c.sw06-host02.1 type veth peer name c.host02-sw06.1
ip link set c.sw06-host02.1 up
ip link set c.host02-sw06.1 up
ip link set c.sw06-host02.1 netns Host-02
ovs-vsctl add-port sw06 c.host02-sw06.1

ip link add c.sw07-host03.1 type veth peer name c.host03-sw07.1
ip link set c.sw07-host03.1 up
ip link set c.host03-sw07.1 up
ip link set c.sw07-host03.1 netns Host-03
ovs-vsctl add-port sw07 c.host03-sw07.1

ip link add c.sw07-host04.1 type veth peer name c.host04-sw07.1
ip link set c.sw07-host04.1 up
ip link set c.host04-sw07.1 up
ip link set c.sw07-host04.1 netns Host-04
ovs-vsctl add-port sw07 c.host04-sw07.1

ip link add c.sw07-host05.1 type veth peer name c.host05-sw07.1
ip link set c.sw07-host05.1 up
ip link set c.host05-sw07.1 up
ip link set c.sw07-host05.1 netns Host-05
ovs-vsctl add-port sw07 c.host05-sw07.1

echo -e '\nDeleting controller from sw00\n
# ovs-vsctl del-controller sw00

# Press Ctrl-C to exit...

echo -e '\nClean_up\n

# ovs-vsctl del-br sw00
# ovs-vsctl del-br sw01
# ovs-vsctl del-br sw02
# ovs-vsctl del-br sw03
# ovs-vsctl del-br sw04
# ovs-vsctl del-br sw05
# ovs-vsctl del-br sw06
# ovs-vsctl del-br sw07

# ip link delete dev c.sw02-sw01.1

# ip link delete dev c.sw03-sw02.1

# ip link delete dev c.sw04-sw01.1

# ip link delete dev c.sw04-sw02.1

# ip link delete dev c.sw05-sw02.1

# ip link delete dev c.sw05-sw03.1

# ip link delete dev c.sw05-sw04.1

# ip link delete dev c.sw06-sw01.1

# ip link delete dev c.sw06-sw04.1

# ip link delete dev c.sw07-sw03.1

# ip link delete dev c.sw07-sw05.1

# ip netns del Host-00
# ip netns del Host-01
# ip netns del Host-02
# ip netns del Host-03
# ip netns del Host-04
# ip netns del Host-05
