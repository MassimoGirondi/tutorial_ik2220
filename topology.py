#!/usr/bin/python

from mininet.topo import Topo

from mininet.cli import CLI
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel

from mininet.node import RemoteController, OVSSwitch
import time
import logging
import os


REMOTE_CONTROLLER_IP = "127.0.0.1"

class MyTopo(Topo):
    log = None

    def __init__(self, **opts):
        # Initialize topology and default options
        Topo.__init__(self, **opts)

        # Add public zone
        sw1 = self.addSwitch('sw1', dpid="1")
        sw2 = self.addSwitch('sw2', dpid="F")
        h1 = self.addHost('h1', ip='100.0.0.10/24')
        h2 = self.addHost('h2', ip='100.0.0.11/24')
        self.addLink(h1, sw1)
        self.addLink(sw1, sw2)
        self.addLink(h2, sw2)

    # The actual start code

    @staticmethod
    def startup(test=None):
        # Tell mininet to print useful information
        setLogLevel('info')
        topo = MyTopo()
        ctrl = RemoteController('c-1', ip=REMOTE_CONTROLLER_IP, port=6633)
        net = Mininet(topo=topo,
                      switch=OVSSwitch,
                      controller=ctrl,
                      autoSetMacs=True,
                      build=True,
                      cleanup=True,
                      autoStaticArp=True)
        net.start()

        topo.log = logging.getLogger(__name__)

        CLI(net)
        net.stop()


if __name__ == '__main__':
    MyTopo.startup(test=None)

