#!/usr/bin/env bash

ips=("192.168.0.1" "173.194.222.113" "87.250.250.242")
port=80

while ((1==1))
do
haveError=0
    for ip in ${ips[@]}
    do
        curl -I --connect-timeout 2 http://${ip}:${port}
        response=$?
        echo "$(date) - ${ip} - ${response}" >> curl.log

        if (($response!=0))
        then
            echo ${ip} >> curl_error.log
            haveError=1
            break
        fi
    done

if (($haveError==1))
then
    echo "Have error, process stopped. Details in curl_error.log"
    break
fi
done