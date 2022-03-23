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

2. Ознакомьтесь с опциями node_exporter и выводом `/metrics` по-умолчанию. Приведите несколько опций, которые вы бы выбрали для базового мониторинга хоста по CPU, памяти, диску и сети.

По умолчанию `node_exporter` включено очень много разных метрик, в выводе с выборкой `node_` почти 1000 строк, часть из них это комментарии.

```shell
vagrant@vagrant:~$ curl http://localhost:9100/metrics | grep -c node_ 
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 61647    0 61647    0     0  4630k      0 --:--:-- --:--:-- --:--:-- 4630k
964
```

Для базового мониторинга хоста по CPU, памяти, диску и сети можно выключить всё, что включено по умолчанию через `--collector.disable-defaults` и включить следующие параметры:
* `--collector.cpu` - предоставляет статистику по CPU.
* `--collector.meminfo` - предоставляет статистику памяти.
* `--collector.filesystem` - предоставляет статистику файловой системы, такую как используемое дисковое пространство.
* `--collector.diskstats` - предоставляет статистику дискового ввода-вывода.
* `--collector.netdev` - предоставляет статистику сетевого интерфейса, такую как переданные байты.
* `--collector.os` - Предоставляет информацию о релизе операционной системы.

3. Ознакомьтесь с метриками, которые по умолчанию собираются [Netdata](https://github.com/netdata/netdata) и с комментариями, которые даны к этим метрикам.

`Netdata` содеджит большое количество метрик:
* `cpu` - общая загрузка процессора (все ядра).
* `load` - текущая загрузка системы, т.е. количество процессов, использующих процессор или ожидающих системных ресурсов (обычно процессора и диска).
* `disk` - общий дисковый ввод-вывод для всех физических дисков. Память, выгружаемая с/на диск.
* `ram` - использование системной оперативной памяти.
* `swap` - использование системной памяти подкачки.
* `network` - общая пропускная способность всех физических сетевых интерфейсов.
* `processes` - системные процессы.
* и многие другие.

Некоторые метрики объединены в группы для более удобного просмотра.

4. Можно ли по выводу `dmesg` понять, осознает ли ОС, что загружена не на настоящем оборудовании, а на системе виртуализации?

В выводе `dmesg` можно найти упоминание о виртуализации от `systemd`.

```shell
vagrant@vagrant:~$ dmesg | grep virtu
[    0.002993] CPU MTRRs all blank - virtualized system.
[    0.067729] Booting paravirtualized kernel on KVM
[    3.267771] systemd[1]: Detected virtualization oracle.
```

Таким образом можно предположить, что ОС понимает, что загружена в виртуальной машине, а не на физическом оборудовании.

5. Как настроен sysctl `fs.nr_open` на системе по-умолчанию? Узнайте, что означает этот параметр. Какой другой существующий лимит не позволит достичь такого числа (`ulimit --help`)

```shell
vagrant@vagrant:~$ sysctl fs.nr_open
fs.nr_open = 1048576
```

`fs.nr_open` - максимальное количество дескрипторов файлов, которые может выделить процесс. Значение по умолчанию равно 1024*1024 (1048576), чего должно быть достаточно для большинства машин.
Изменить для текущей сесии можно через `ulimit -n`, для групп и отдельных пользователей через конфигурационный файл `/etc/security/limits.conf`.
Максимальный лимит обычно закладывается при сборке ядра и сделать его больше через `ulimit -n` не удастся.

6. Запустите любой долгоживущий процесс (не `ls`, который отработает мгновенно, а, например, `sleep 1h`) в отдельном неймспейсе процессов; покажите, что ваш процесс работает под `PID 1` через `nsenter`.

Запустим `bash` в отдельном процессе.

```shell
vagrant@vagrant:~$ sudo unshare -f --pid --mount-proc /bin/bash
root@vagrant:/home/vagrant# ps aux
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1  0.0  0.3   7236  3900 pts/0    S    13:59   0:00 /bin/bash
root           8  0.0  0.3   8892  3344 pts/0    R+   13:59   0:00 ps aux
```

Найдём его в дереве процессов и подключимся через `nsenter`.

```shell
vagrant@vagrant:~$ ps au --forest
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
vagrant     1588  0.0  0.4   7360  4160 pts/1    Ss   14:01   0:00 -bash
vagrant     1604  0.0  0.3   8892  3316 pts/1    R+   14:02   0:00  \_ ps au --forest
vagrant     1484  0.0  0.4   7492  4364 pts/0    Ss   13:54   0:00 -bash
root        1532  0.0  0.4   9264  4548 pts/0    S    13:59   0:00  \_ sudo unshare -f --pid --mount-proc /bin/bash
root        1534  0.0  0.0   5480   528 pts/0    S    13:59   0:00      \_ unshare -f --pid --mount-proc /bin/bash
root        1535  0.0  0.3   7236  3900 pts/0    S+   13:59   0:00          \_ /bin/bash
root         673  0.0  0.1   5828  1804 tty1     Ss+  13:53   0:00 /sbin/agetty -o -p -- \u --noclear tty1 linux


vagrant@vagrant:~$ sudo nsenter -t 1535 -p -m
root@vagrant:/# ps aux
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1  0.0  0.3   7236  3900 pts/0    S+   13:59   0:00 /bin/bash
root           9  0.0  0.4   7236  4124 pts/1    S    14:05   0:00 -bash
root          20  0.0  0.3   8892  3284 pts/1    R+   14:05   0:00 ps aux
```

7. Найдите информацию о том, что такое `:(){ :|:& };:`. Вызов `dmesg` расскажет, какой механизм помог автоматической стабилизации. Как настроен этот механизм по-умолчанию, и как изменить число процессов, которое можно создать в сессии?

Данная команда - это `fork bomb` она порождает большое количество собственных копий и тем самым пытается заполнить свободное место в списке активных процессов, её можно разобрать на следующие части:

```shell
:()         # define a function named :, () defines a function in bash
{
      : | :;  # the pipe needs two instances of this function, which forks two shells
}
;           # end function definition
:           # run it
```

В выводе `dmesg` - можно увидеть данное сообщение об отклонении форка.

``` shell
[  916.422595] cgroup: fork rejected by pids controller in /user.slice/user-1000.slice/session-6.scope
```

Количество процессов можно изменить через `ulimit -u`.
