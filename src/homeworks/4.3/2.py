#!/usr/bin/env python3
import socket
import time
import json
import yaml

hosts = ['drive.google.com', 'mail.google.com', 'google.com']
ip_hosts = {}

filename = 'hosts_config'

while True:
    data = []
    for host in hosts:
        ip = socket.gethostbyname(host)
        if ip_hosts.get(host, ip) == ip:
            print('{} - {}'.format(host, ip))
        else:
            print('[ERROR] {} IP mismatch: {} {}'.format(host, ip_hosts.get(host), ip))
        ip_hosts[host] = ip

        data.append({host:ip})

    with open(filename + ".json",'w') as json_data:
        json.dump(data, json_data)

    with open(filename + ".yaml",'w') as yaml_data:
        yaml_data.write(yaml.dump(data))
    time.sleep(10)