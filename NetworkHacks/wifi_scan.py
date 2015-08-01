#!/usr/bin/env python

from pythonwifi.iwlibs import Wireless

wifi = Wireless("en0")

for ap in wifi.scan():
    print ap.sprintf("SSID: %essid%")
