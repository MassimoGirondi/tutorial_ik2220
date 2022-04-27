# IK2220 - Pox + Click

This repository contains some simple examples on how you can integrate POX with Click.

The mininet topology is composed by 2 hosts connected via 2 chained switches:

```
        ┌───────────────────┐
        │  POX Controller   │
        │                   │
        └──┬──────────────┬─┘
           │              │
           ▼              ▼
        ┌──────┐     ┌──────┐
       1│ SW1  │2   1│ SW2  │2
    ┌───┤id=0x1├─────┤id=0xf├──┐
    │   └──────┘     └──────┘  │
   0│                          │0
 ┌──┴──┐                    ┌──┴──┐
 │ H1  │                    │ H2  │
 └─────┘                    └─────┘

 ```

 We'll replace SW2 with a Click-based forwarder, which will steal packets and do the forwarding instead of OpenVSwitch.

 * `controller_base.py` is a simple POX controller that will start the standard `LearningSwitch` for all switches
 * `controller_click_base.py` replaces the second controller/switch with Click
 * `controller.py` is a complete example with also process termination management
 * `forwarder.click` is a simple L2 forwarder with 2 ports (a.k.a. a bridge)
 * `forwarder.click` is a L2 forwarder demonstrating Print, Script and DriverManager elements


# How to use

* Start your network with `sudo python topology.py`
* Start a controller with `PYTHONPATH=. python /opt/ik2220/pox/pox.py controller`
* Send some packets from the mininet console: `h1 ping h2`
* Have fun!

# Copyright

 (C) Massimo Girondi 2022 - girondi@kth.se - BY-NC-SA 4.0
