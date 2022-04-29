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

        # Handle kill signals
        signal.signal(signal.SIGTERM, self.handle_kill)
        signal.signal(signal.SIGINT, self.handle_kill)

    def handle_kill(self, sig, frame):
        # Instead of this, go through click_pids! We save them for a reason!
        print("Got kill signal. Notify all click processes")
        subprocess.check_output(
            "sudo killall -SIGTERM click || true", shell=True)
        exit(0)

    def launch_click(self, dpid, configuration, name):
        # Before launching you may want to kill pre-existing click processes
        # Something like (the square brackets are needed to not match grep itself)
        # PUT ONLY ONE CHARACTER IN THE SQUARE PARENTHESIS!

        #subprocess.check_output(
        #    "sudo kill -SIGTERM `ps -ef | grep '[.]click' | awk '{print $2}'` || true", shell=True)

        # Or simply, all click processes
        subprocess.check_output(
            "sudo killall -SIGTERM click || true", shell=True)

        # Simply start click, send to background
        cmd = "sudo click forwarder.click &"

        # Override the variables
        # cmd = "sudo click forwarder.click PORT1=%s PORT2=%s &" % ("sw2-eth1", "sw2-eth2")

        # Send output to a file (elements print will still come on POX console)
        # cmd = "sudo click forwarder.click > /tmp/click.out &"

        # Send also stderr to a file
        # cmd = "sudo click forwarder_counters.click > /tmp/click.out 2>&1 &"

        # Or, more elegantly, you could capture the output directly by changing Popen parameters

        log.info("Launching click for " + name + " with command " + cmd)
        p = subprocess.Popen(cmd, shell=True)
        log.info("Click launched for " + name + " with PID " + str(p.pid))
        self.click_pids[dpid] = p.pid

    def _handle_ConnectionUp(self, event):
        # Select the right component to handle the switch given event.dpid
        log.info("Connection from switch with DPID %d" % event.dpid)

        if(event.dpid == 0x1):
            # This is a normal switch. Start the LearningSwitch
            log.info("Starting a LearningSwitch for %d" % event.dpid)
            LearningSwitch(event.connection, False)
        elif(event.dpid == 0xF):
            # This is the click switch. Launch it
            log.info("Starting a Click process for %d" % event.dpid)
            self.launch_click(event.dpid, "switch.click", "switch")
        else:
            log.info("Unrecognized dpid %d from switch. No component will be associated to the switch" % (
                event.dpid,))


def launch():
    log.info("Starting %s" % __file__)
    core.registerNew(Controller)
