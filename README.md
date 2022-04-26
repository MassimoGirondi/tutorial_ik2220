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


# Copyright

 (C) Massimo Girondi 2022 - girondi@kth.se - BY-NC-SA 4.0
