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

    def _handle_ConnectionUp(self, event):
	    log.info("Starting a LearningSwitch for %d" % event.dpid)
            LearningSwitch(event.connection, False)

def launch():
    log.info("Starting %s" % __file__)
    core.registerNew(Controller)

