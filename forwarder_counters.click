define($PORT1 sw2-eth1, $PORT2 sw2-eth2)
Script(print "Click forwarder on $PORT1 $PORT2")


elementclass L2Forwarder {$port|
	input
	-> cnt::Counter
	->Strip(14)
	->CheckIPHeader2()
	->IPPrint($PORT1)
	->Unstrip(14)
	->Queue
	->output
}

fd1::FromDevice($PORT1, SNIFFER false, METHOD LINUX, PROMISC true)
fd2::FromDevice($PORT2, SNIFFER false, METHOD LINUX, PROMISC true)
td1::ToDevice($PORT1, METHOD LINUX)
td2::ToDevice($PORT2, METHOD LINUX)
fd1->fwd1::L2Forwarder($port1)->td2
fd2->fwd2::L2Forwarder($port2)->td1


DriverManager(pause,
	print "Packets from ${PORT1}: $(fwd1/cnt.count)",
	print "Packets from ${PORT2}: $(fwd2/cnt.count)",
)
