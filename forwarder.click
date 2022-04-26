define($PORT1 sw2-eth1, $PORT2 sw2-eth2)

fd1::FromDevice($PORT1, SNIFFER false, METHOD LINUX, PROMISC true)
fd2::FromDevice($PORT2, SNIFFER false, METHOD LINUX, PROMISC true)
td1::ToDevice($PORT1, METHOD LINUX)
td2::ToDevice($PORT2, METHOD LINUX)

// Take packets on one port, Print, and send to the other

fd1->Strip(14)->CheckIPHeader2->IPPrint->Unstrip(14)->Queue->td2
fd2->Strip(14)->CheckIPHeader2->IPPrint->Unstrip(14)->Queue->td1

