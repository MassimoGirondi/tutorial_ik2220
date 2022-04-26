#!/bin/python2
from pox.core import core
from forwarding.l2_learning import LearningSwitch
import pox.lib.packet as pkt
import os
import subprocess
import time
import signal


log = core.getLogger()


class Controller:

    def __init__(self):
        core.openflow.addListeners(self)
        self.click_pids = {}
    
    def launch_click(self, dpid, configuration, name):
	# Simple click, send to background
	cmd = "sudo click forwarder.click &"

        log.info("Launching click for " + name + " with command " + cmd)
        p = subprocess.Popen(cmd, shell = True)
        log.info("Click launched for " + name + " with PID " + str(p.pid))
        self.click_pids[dpid] = p.pid


    def _handle_ConnectionUp(self, event):
        # Select the right component to handle the switch given event.dpid
	log.info("Connection from switch with DPID %d" % event.dpid)

        if(event.dpid  == 0x1):
            # This is a normal switch. Start the LearningSwitch
	    log.info("Starting a LearningSwitch for %d" % event.dpid)
            LearningSwitch(event.connection, False)
        elif(event.dpid == 0xF):
	    log.info("Starting a Click process for %d" % event.dpid)
            # This is the click switch. Launch it
            self.launch_click(event.dpid, "fowarder.click", "switch")
            pass
        else:
            log.info("Unrecognized dpid %d from switch. No component will be associated to the switch" % (
                event.dpid,))


def launch():
    log.info("Starting %s" % __file__)
    core.registerNew(Controller)

