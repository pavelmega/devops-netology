#!/usr/bin/env python3
import socket
import time

hosts = ['drive.google.com', 'mail.google.com', 'google.com']
ip_hosts = {}
while True:
    for host in hosts:
        ip = socket.gethostbyname(host)
        if ip_hosts.get(host, ip) == ip:
            print('{} - {}'.format(host, ip))
        else:
            print('[ERROR] {} IP mismatch: {} {}'.format(host, ip_hosts.get(host), ip))
        ip_hosts[host] = ip
    time.sleep(1)