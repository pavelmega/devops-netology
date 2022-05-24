#!/usr/bin/env bash

ips=("192.168.0.1" "173.194.222.113" "87.250.250.242")
port=80

for i in {1..5}
do
    for ip in ${ips[@]}
    do
        curl -I --connect-timeout 2 http://${ip}:${port}
        response=$?
        echo "$(date) - ${ip} - ${response}" >> curl.log
    done
done