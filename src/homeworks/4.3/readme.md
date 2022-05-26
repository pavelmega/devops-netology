# Результат выполнения домашнего задания ["4.3. Языки разметки JSON и YAML"](https://github.com/netology-code/sysadm-homeworks/tree/devsys10/04-script-03-yaml)

## Обязательная задача 1
Мы выгрузили JSON, который получили через API запрос к нашему сервису:
```
    { "info" : "Sample JSON output from our service\t",
        "elements" :[
            { "name" : "first",
            "type" : "server",
            "ip" : 7175 
            }
            { "name" : "second",
            "type" : "proxy",
            "ip : 71.78.22.43
            }
        ]
    }
```
  Нужно найти и исправить все ошибки, которые допускает наш сервис

Решение:
```json
{
    "info": "Sample JSON output from our service\t",
    "elements": [
        {
            "name": "first",
            "type": "server",
            "ip": 7175
        },
        {
            "name": "second",
            "type": "proxy",
            "ip": "71.78.22.43"
        }
    ]
}
```

## Обязательная задача 2
В прошлый рабочий день мы создавали скрипт, позволяющий опрашивать веб-сервисы и получать их IP. К уже реализованному функционалу нам нужно добавить возможность записи JSON и YAML файлов, описывающих наши сервисы. Формат записи JSON по одному сервису: `{ "имя сервиса" : "его IP"}`. Формат записи YAML по одному сервису: `- имя сервиса: его IP`. Если в момент исполнения скрипта меняется IP у сервиса - он должен так же поменяться в yml и json файле.

### Ваш скрипт:

[Скрипт](2.py)

```python
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
```

### Вывод скрипта при запуске при тестировании:
```
./2.py
google.com - 142.250.74.142
drive.google.com - 173.194.222.194
mail.google.com - 216.58.211.5
[ERROR] google.com IP mismatch: 142.250.74.142 142.250.74.78
drive.google.com - 173.194.222.194
mail.google.com - 216.58.211.5
google.com - 142.250.74.78
```

### json-файл(ы), который(е) записал ваш скрипт:
```json
[{"drive.google.com": "173.194.222.194"}, {"mail.google.com": "216.58.211.5"}, {"google.com": "142.250.74.78"}]
```

### yml-файл(ы), который(е) записал ваш скрипт:
```yaml
- drive.google.com: 173.194.222.194
- mail.google.com: 216.58.211.5
- google.com: 142.250.74.78
```