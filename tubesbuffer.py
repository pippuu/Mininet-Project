#!/usr/bin/env python
from mininet.net import Mininet
from mininet.link import TCLink, Link, Intf
from mininet.cli import CLI
from mininet.topo import Topo
from mininet.log import setLogLevel
from mininet.node import Host
import os

# Initial declaration
net = Mininet(link = TCLink)

# Creating object host
hA = net.addHost('hA')
hB = net.addHost('hB')

# Creating object router
r1 = net.addHost('r1')
r2 = net.addHost('r2')
r3 = net.addHost('r3')
r4 = net.addHost('r4')

# Creating link for each object
net.addLink(hA,r1,intfName1 = 'hA-eth0',intfName2 = 'r1-eth0',cls = TCLink, bw = 1,max_queue_size = 20,use_htb = True)
net.addLink(hA,r2,intfName1 = 'hA-eth1',intfName2 = 'r2-eth1',cls = TCLink, bw = 1,max_queue_size = 20,use_htb = True)
net.addLink(hB,r3,intfName1 = 'hB-eth0',intfName2 = 'r3-eth0',cls = TCLink, bw = 1,max_queue_size = 20,use_htb = True)
net.addLink(hB,r4,intfName1 = 'hB-eth1',intfName2 = 'r4-eth1',cls = TCLink, bw = 1,max_queue_size = 20,use_htb = True)
net.addLink(r1,r3,intfName1 = 'r1-eth1',intfName2 = 'r3-eth1',cls = TCLink, bw = 0.5,max_queue_size = 20,use_htb = True)
net.addLink(r1,r4,intfName1 = 'r1-eth2',intfName2 = 'r4-eth2',cls = TCLink, bw = 1,max_queue_size = 20,use_htb = True)
net.addLink(r2,r4,intfName1 = 'r2-eth0',intfName2 = 'r4-eth0',cls = TCLink, bw = 0.5,max_queue_size = 20,use_htb = True)
net.addLink(r2,r3,intfName1 = 'r2-eth2',intfName2 = 'r3-eth2',cls = TCLink, bw = 1,max_queue_size = 20,use_htb = True)

# Build network
net.build()

# Config IP 
hA.cmd("ifconfig hA-eth0 190.100.0.1 netmask 255.255.255.252")
hA.cmd("ifconfig hA-eth1 190.100.0.22 netmask 255.255.255.252")
hB.cmd("ifconfig hB-eth0 190.100.0.10 netmask 255.255.255.252")
hB.cmd("ifconfig hB-eth1 190.100.0.13 netmask 255.255.255.252")
r1.cmd("ifconfig r1-eth0 190.100.0.2 netmask 255.255.255.252")
r1.cmd("ifconfig r1-eth1 190.100.0.5 netmask 255.255.255.252")
r1.cmd("ifconfig r1-eth2 190.100.0.26 netmask 255.255.255.252")
r2.cmd("ifconfig r2-eth0 190.100.0.18 netmask 255.255.255.252")
r2.cmd("ifconfig r2-eth1 190.100.0.21 netmask 255.255.255.252")
r2.cmd("ifconfig r2-eth2 190.100.0.29 netmask 255.255.255.252")
r3.cmd("ifconfig r3-eth0 190.100.0.9 netmask 255.255.255.252")
r3.cmd("ifconfig r3-eth1 190.100.0.6 netmask 255.255.255.252")
r3.cmd("ifconfig r3-eth2 190.100.0.30 netmask 255.255.255.252")
r4.cmd("ifconfig r4-eth0 190.100.0.17 netmask 255.255.255.252")
r4.cmd("ifconfig r4-eth1 190.100.0.14 netmask 255.255.255.252")
r4.cmd("ifconfig r4-eth2 190.100.0.25 netmask 255.255.255.252")

# Config router
r1.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
r2.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
r3.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
r4.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")	

# Static routing (Host)
hA.cmd("ip rule add from 190.100.0.1 table 1")
hA.cmd("ip rule add from 190.100.0.22 table 2")
hA.cmd("ip route add 190.100.0.0/30 dev hA-eth0 scope link table 1")
hA.cmd("ip route add default via 190.100.0.2 dev hA-eth0 table 1")
hA.cmd("ip route add 190.100.0.20/30 dev hA-eth1 scope link table 2")
hA.cmd("ip route add default via 190.100.0.21 dev hA-eth1 table 2")
hA.cmd("ip route add default scope global nexthop via 190.100.0.2 dev hA-eth0")
hB.cmd("ip rule add from 190.100.0.10 table 3")
hB.cmd("ip rule add from 190.100.0.13 table 4")
hB.cmd("ip route add 190.100.0.8/30 dev hB-eth0 scope link table 3")
hB.cmd("ip route add default via 190.100.0.9 dev hB-eth0 table 3")
hB.cmd("ip route add 190.100.0.12/30 dev hB-eth1 scope link table 4")
hB.cmd("ip route add default via 190.100.0.14 dev hB-eth1 table 4")
hB.cmd("ip route add default scope global nexthop via 190.100.0.9 dev hB-eth0")

# Static routing (Router)
r1.cmd("route add -net 190.100.0.8/30 gw 190.100.0.6")
r1.cmd("route add -net 190.100.0.12/30 gw 190.100.0.25")
r1.cmd("route add -net 190.100.0.28/30 gw 190.100.0.6")
r1.cmd("route add -net 190.100.0.20/30 gw 190.100.0.25")
r1.cmd("route add -net 190.100.0.16/30 gw 190.100.0.25")

r2.cmd("route add -net 190.100.0.8/30 gw 190.100.0.30")
r2.cmd("route add -net 190.100.0.12/30 gw 190.100.0.17")
r2.cmd("route add -net 190.100.0.24/30 gw 190.100.0.17")
r2.cmd("route add -net 190.100.0.4/30 gw 190.100.0.30")
r2.cmd("route add -net 190.100.0.0/30 gw 190.100.0.30")

r3.cmd("route add -net 190.100.0.12/30 gw 190.100.0.29")
r3.cmd("route add -net 190.100.0.24/30 gw 190.100.0.5")
r3.cmd("route add -net 190.100.0.16/30 gw 190.100.0.29")
r3.cmd("route add -net 190.100.0.0/30 gw 190.100.0.5")
r3.cmd("route add -net 190.100.0.20/30 gw 190.100.0.29")

r4.cmd("route add -net 190.100.0.8/30 gw 190.100.0.26")
r4.cmd("route add -net 190.100.0.28/30 gw 190.100.0.18")
r4.cmd("route add -net 190.100.0.4/30 gw 190.100.0.26")
r4.cmd("route add -net 190.100.0.0/30 gw 190.100.0.26")
r4.cmd("route add -net 190.100.0.20/30 gw 190.100.0.18")

# Setting up Command Line Interface
CLI(net)

# Stop network
net.stop()

# Clear cache
os.system('mn -c')


