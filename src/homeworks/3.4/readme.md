# Результат выполнения домашнего задания ["3.4. Операционные системы, лекция 2"](https://github.com/netology-code/sysadm-homeworks/tree/devsys10/03-sysadmin-04-os)

1. Используя знания из лекции по systemd, создайте самостоятельно простой unit-файл для [node_exporter](https://github.com/prometheus/node_exporter)

Для начала необходимо установить `node_exporter`. Сделать это можно воспользовавшись [официальной документацией](https://prometheus.io/docs/guides/node-exporter/#installing-and-running-the-node-exporter). После установки добавим его в `/usr/local/bin/`, чтобы свободно вызывать из консоли:

```shell
wget https://github.com/prometheus/node_exporter/releases/download/v1.3.1/node_exporter-1.3.1.linux-amd64.tar.gz
tar xvfz node_exporter-1.3.1.linux-amd64.tar.gz
cd node_exporter-1.3.1.linux-amd64

sudo mv node_exporter /usr/local/bin
```
Для проверки того, что всё установилось и работает можно воспользоваться командой проверки версии `node_exporter -v`:

```shell
vagrant@vagrant:~$ node_exporter --version
node_exporter, version 1.3.1 (branch: HEAD, revision: a2321e7b940ddcff26873612bccdf7cd4c42b6b6)
  build user:       root@243aafa5525c
  build date:       20211205-11:09:49
  go version:       go1.17.3
  platform:         linux/amd64
```

После можно уже приступить к созданию unit-файла, для этого изучим документацию `man systemd.unit` и создадим файл в `/etc/systemd/system`:

```shell
sudo touch /etc/systemd/system/node_exporter.service
```

 Т.к. мы уже ранее добавили node_exporter в `/usr/local/bin`, поэтому и вызов будем делать оттуда `ExecStart=/usr/local/bin/node_exporter`. Наполним файл следующим содежимым:

```file
[Unit]
Description=Node exporter service of Prometheus
StartLimitIntervalSec=0

[Service]
Type=simple
Restart=always
RestartSec=1
User=vagrant
ExecStart=/usr/local/bin/node_exporter

[Install]
WantedBy=multi-user.target
```

Затем запустим сервис, проверим его статус:

```shell
vagrant@vagrant:~$ sudo systemctl start node_exporter.service
vagrant@vagrant:~$ sudo systemctl status node_exporter.service
● node_exporter.service - Node exporter service of Prometheus
     Loaded: loaded (/etc/systemd/system/node_exporter.service; disabled; vendor preset: enabled)
     Active: active (running) since Tue 2022-03-22 15:05:51 UTC; 8s ago
   Main PID: 6499 (node_exporter)
      Tasks: 5 (limit: 1071)
     Memory: 2.6M
     CGroup: /system.slice/node_exporter.service
             └─6499 /usr/local/bin/node_exporter

Mar 22 15:05:51 vagrant node_exporter[6499]: ts=2022-03-22T15:05:51.598Z caller=node_exporter.go:115 level=info collector=thermal_zone
Mar 22 15:05:51 vagrant node_exporter[6499]: ts=2022-03-22T15:05:51.598Z caller=node_exporter.go:115 level=info collector=time
Mar 22 15:05:51 vagrant node_exporter[6499]: ts=2022-03-22T15:05:51.598Z caller=node_exporter.go:115 level=info collector=timex
Mar 22 15:05:51 vagrant node_exporter[6499]: ts=2022-03-22T15:05:51.598Z caller=node_exporter.go:115 level=info collector=udp_queues
Mar 22 15:05:51 vagrant node_exporter[6499]: ts=2022-03-22T15:05:51.598Z caller=node_exporter.go:115 level=info collector=uname
Mar 22 15:05:51 vagrant node_exporter[6499]: ts=2022-03-22T15:05:51.598Z caller=node_exporter.go:115 level=info collector=vmstat
Mar 22 15:05:51 vagrant node_exporter[6499]: ts=2022-03-22T15:05:51.598Z caller=node_exporter.go:115 level=info collector=xfs
Mar 22 15:05:51 vagrant node_exporter[6499]: ts=2022-03-22T15:05:51.598Z caller=node_exporter.go:115 level=info collector=zfs
Mar 22 15:05:51 vagrant node_exporter[6499]: ts=2022-03-22T15:05:51.598Z caller=node_exporter.go:199 level=info msg="Listening on" addres>
Mar 22 15:05:51 vagrant node_exporter[6499]: ts=2022-03-22T15:05:51.601Z caller=tls_config.go:195 level=info msg="TLS is disabled." http2>
lines 1-19/19 (END)
```

Проверим работоспособность самого приложения, для этого сделаем запрос для получения статус кода на `http://localhost:9100/metrics`.

```shell
vagrant@vagrant:~$ curl -I http://localhost:9100/metric
HTTP/1.1 200 OK
Date: Tue, 22 Mar 2022 15:08:01 GMT
Content-Length: 150
Content-Type: text/html; charset=utf-8
```

Остановим работу и проверим статус:

```shell
vagrant@vagrant:~$ sudo systemctl stop node_exporter.service
vagrant@vagrant:~$ sudo systemctl status node_exporter.service
● node_exporter.service - Node exporter service of Prometheus
     Loaded: loaded (/etc/systemd/system/node_exporter.service; disabled; vendor preset: enabled)
     Active: inactive (dead)

Mar 22 15:05:51 vagrant node_exporter[6499]: ts=2022-03-22T15:05:51.598Z caller=node_exporter.go:115 level=info collector=udp_queues
Mar 22 15:05:51 vagrant node_exporter[6499]: ts=2022-03-22T15:05:51.598Z caller=node_exporter.go:115 level=info collector=uname
Mar 22 15:05:51 vagrant node_exporter[6499]: ts=2022-03-22T15:05:51.598Z caller=node_exporter.go:115 level=info collector=vmstat
Mar 22 15:05:51 vagrant node_exporter[6499]: ts=2022-03-22T15:05:51.598Z caller=node_exporter.go:115 level=info collector=xfs
Mar 22 15:05:51 vagrant node_exporter[6499]: ts=2022-03-22T15:05:51.598Z caller=node_exporter.go:115 level=info collector=zfs
Mar 22 15:05:51 vagrant node_exporter[6499]: ts=2022-03-22T15:05:51.598Z caller=node_exporter.go:199 level=info msg="Listening on" addres>
Mar 22 15:05:51 vagrant node_exporter[6499]: ts=2022-03-22T15:05:51.601Z caller=tls_config.go:195 level=info msg="TLS is disabled." http2>
Mar 22 15:10:25 vagrant systemd[1]: Stopping Node exporter service of Prometheus...
Mar 22 15:10:25 vagrant systemd[1]: node_exporter.service: Succeeded.
Mar 22 15:10:25 vagrant systemd[1]: Stopped Node exporter service of Prometheus.
lines 1-14/14 (END)
```

Для добавления опций через внешний файл необходимо добавить в файл переменную окружения `EXTRA_OPTS` с каким-либо значением из поддерживаемых, например `--collector.cpu.info`. И отредактировать unit-файл:

```shell
vagrant@vagrant:/usr/local$ sudo mkdir -p /usr/local/node_exporter/
vagrant@vagrant:/usr/local$ sudo touch /usr/local/node_exporter/conf
vagrant@vagrant:/usr/local$ sudo chmod +r /usr/local/node_exporter/conf
vagrant@vagrant:/usr/local$ echo "EXTRA_OPTS=--collector.cpu.info" | tee sudo /usr/local/node_exporter/conf
vagrant@vagrant:/usr/local$ cat /usr/local/node_exporter/conf
EXTRA_OPTS=--collector.cpu.info
```

В unit-файле нас интересует секция `[Service]`, а в ней две строки с данными:
* Переменная `EnvironmentFile`. В неё следует добавить путь до конфигурационного файла
* В переменную `ExecStart` добавить вывод переменной окружения `$EXTRA_OPTS`

Таким образом сам unit-файл будет выглядеть следующим образом:

```file
[Unit]
Description=Node exporter service of Prometheus
StartLimitIntervalSec=0

[Service]
Type=simple
Restart=always
RestartSec=1
User=vagrant
EnvironmentFile=-/usr/local/node_exporter/conf
ExecStart=/usr/local/bin/node_exporter $EXTRA_OPTS

[Install]
WantedBy=multi-user.target
```

Проверим, что приложение запустилось с нужным флагом:

```shell
vagrant@vagrant:/usr/local$ sudo systemctl daemon-reload
vagrant@vagrant:/usr/local$ sudo systemctl start node_exporter.service
vagrant@vagrant:/usr/local$ sudo systemctl status node_exporter.service
● node_exporter.service - Node exporter service of Prometheus
     Loaded: loaded (/etc/systemd/system/node_exporter.service; disabled; vendor preset: enabled)
     Active: active (running) since Tue 2022-03-22 15:44:49 UTC; 4s ago
   Main PID: 6810 (node_exporter)
      Tasks: 5 (limit: 1071)
     Memory: 2.4M
     CGroup: /system.slice/node_exporter.service
             └─6810 /usr/local/bin/node_exporter --collector.cpu.info

Mar 22 15:44:49 vagrant node_exporter[6810]: ts=2022-03-22T15:44:49.834Z caller=node_exporter.go:115 level=info collector=thermal_zone
Mar 22 15:44:49 vagrant node_exporter[6810]: ts=2022-03-22T15:44:49.834Z caller=node_exporter.go:115 level=info collector=time
Mar 22 15:44:49 vagrant node_exporter[6810]: ts=2022-03-22T15:44:49.834Z caller=node_exporter.go:115 level=info collector=timex
Mar 22 15:44:49 vagrant node_exporter[6810]: ts=2022-03-22T15:44:49.834Z caller=node_exporter.go:115 level=info collector=udp_queues
Mar 22 15:44:49 vagrant node_exporter[6810]: ts=2022-03-22T15:44:49.834Z caller=node_exporter.go:115 level=info collector=uname
Mar 22 15:44:49 vagrant node_exporter[6810]: ts=2022-03-22T15:44:49.834Z caller=node_exporter.go:115 level=info collector=vmstat
Mar 22 15:44:49 vagrant node_exporter[6810]: ts=2022-03-22T15:44:49.834Z caller=node_exporter.go:115 level=info collector=xfs
Mar 22 15:44:49 vagrant node_exporter[6810]: ts=2022-03-22T15:44:49.834Z caller=node_exporter.go:115 level=info collector=zfs
Mar 22 15:44:49 vagrant node_exporter[6810]: ts=2022-03-22T15:44:49.834Z caller=node_exporter.go:199 level=info msg="Listening on" addres>
Mar 22 15:44:49 vagrant node_exporter[6810]: ts=2022-03-22T15:44:49.837Z caller=tls_config.go:195 level=info msg="TLS is disabled." http2>
lines 1-19/19 (END)
```

Для добавления процесса в автозагрузку необходимо выполнить команду `sudo systemctl enable node_exporter.service`.

```shell
vagrant@vagrant:~$ sudo systemctl enable node_exporter.service
Created symlink /etc/systemd/system/multi-user.target.wants/node_exporter.service → /etc/systemd/system/node_exporter.service.
```
После чего сервис будет запускаться каждый раз при старте системы.
