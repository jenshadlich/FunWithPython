#!/usr/bin/python
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import sniff, ARP
import sys

ip_to_mac = {}

def arp_watch_callback(packet):
    print "watch_arp"

    if ARP in packet and packet[ARP].op in (1,2):
        packet.sprintf("%ARP.hwsrc% %ARP.psrc%")

        if ip_to_mac.get(packet[ARP].psrc) is None:
            print "new device"
            ip_to_mac[packet[ARP].psrc] = packet[ARP].hwsrc

        elif ip_to_mac[packet[ARP].psrc] and ip_to_mac[packet[ARP].psrc] != packet[ARP].hwsrc:
            print "device changed ip"
            ip_to_mac[packet[ARP].psrc] = packet[ARP].hwsrc

if len(sys.argv) < 2:
    print sys.argv[0] + " <iface>"
    sys.exit(0)

sniff(prn=arp_watch_callback, filter="arp", iface=sys.argv[1], store=0)
