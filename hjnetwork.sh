#!/usr/bin/bash

service network-manager stop
ifconfig wlp4s0 192.168.19.1/24 up
service isc-dhcp-server start
hostapd -d /home/hejie/hostapd.conf
