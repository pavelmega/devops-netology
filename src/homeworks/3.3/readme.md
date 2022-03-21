Результат выполнения домашнего задания
["3.3. Операционные системы, лекция 1"](https://github.com/netology-code/sysadm-homeworks/blob/devsys10/03-sysadmin-03-os/README.md)

1. Какой системный вызов делает команда `cd`?

Для поиска придётся перенаправить поток `stderr` в `stdout`, а также воспользоватся выводом в `less` или сразу выполнить поиск через `grep`.

```shell
strace /bin/bash -c 'cd /tmp' 2>&1 | grep tmp
```
В трейсе видно, что комада `cd` выполняет системный вызов `chdir("/tmp")`.

2. Используя strace выясните, где находится база данных file на основании которой она делает свои догадки.

При использовании `strace` на любом файле в выводе будет присутсвовать

```
openat(AT_FDCWD, "/usr/share/misc/magic.mgc", O_RDONLY) = 3
```

Возможно тут и находится база знаний, на основе которой `strace` и делает свои догадки.

3. Основываясь на знаниях о перенаправлении потоков предложите способ обнуления открытого удаленного файла (чтобы освободить место на файловой системе).

Пример удалённого файла в выводе `lsof`:

```
php       17549                  root   16w      REG              253,1 2681235117     913772 /app/storage/logs/cron/some.log (deleted)
```

Если мы знаем `PID` процесса, то мы можем найти файл на диске с учётом того, что процессы пишут свои файлы в директории `/proc/<PID>/fd`

```
ls -la /proc/17549/fd/

total 0
dr-x------ 2 vagrant vagrant  0 Feb 16 20:22 .
dr-xr-xr-x 9 vagrant vagrant  0 Feb 16 20:22 ..
lrwx------ 1 vagrant vagrant 64 Feb 16 20:22 0 -> /dev/pts/0
lr-x------ 1 vagrant vagrant 64 Feb 16 20:22 1 -> /app/storage/logs/cron/some.log
```

Здесь видно, что искомый файл удерживается соединением потока `1`. Для зануления данного файла достаточно направить пустую строку в него:

```shell
echo "" > /proc/17549/fd/1
```

4. Занимают ли зомби-процессы какие-то ресурсы в ОС (CPU, RAM, IO)?

Зомби-процессы не используют никаких ресурсов, за ними остаётся только идентификатор процесса.

5. На какие файлы вы увидели вызовы группы `open` за первую секунду работы утилиты `opensnoop`

В перые секунды работы был получен следующий вывод:

```shell
vagrant@vagrant:~$ sudo opensnoop-bpfcc 

PID    COMM               FD ERR PATH
385    systemd-udevd      14   0 /sys/fs/cgroup/unified/system.slice/systemd-udevd.service/cgroup.procs
385    systemd-udevd      14   0 /sys/fs/cgroup/unified/system.slice/systemd-udevd.service/cgroup.threads
835    vminfo              4   0 /var/run/utmp
632    dbus-daemon        -1   2 /usr/local/share/dbus-1/system-services
632    dbus-daemon        20   0 /usr/share/dbus-1/system-services
632    dbus-daemon        -1   2 /lib/dbus-1/system-services
632    dbus-daemon        20   0 /var/lib/snapd/dbus-1/system-services/
```
6. Какой системный вызов использует `uname -a`? Приведите цитату из man по этому системному вызову, где описывается альтернативное местоположение в `/proc`, где можно узнать версию ядра и релиз ОС.

Утилита использует системный вызов `uname`

```
vagrant@vagrant:~$ strace uname -a 2>&1 | grep uname
execve("/usr/bin/uname", ["uname", "-a"], 0x7fffa3157318 /* 32 vars */) = 0
```

Мануал к нему можно посмотреть через `man 2 uname`. На виртуальной машине не оказалось мануалов для системных вызовов, они содержатся в `manpages-dev`. На виртуальную машину можно отдельно установить данный пакет через `sudo apt intall manpages-dev`.

Цитата из мануала про `/proc`, полученная с хост-машины:
> Part of the utsname information is also accessible via /proc/sys/kernel/{ostype, hostname,  osrelease,  ver‐sion, domainname}.

7. Чем отличается последовательность команд через `;` и через `&&` в bash? Есть ли смысл использовать в bash `&&`, если применить `set -e`?

При использовании `;` команда не будет дожидаться определённого статуса выполнения предыдущей, она просто запустит последовательное выполнение следующей команды, а использование `&&` заставит команду ожидать статуса выполнения предыдущей и запустится только в случае выхода из первой с нулевым статусом:

> A list is a sequence of one or more pipelines separated by one of the operators ;, &, &&, or ||, and optionally terminated by one of ;, &, or <newline>.
> Of these list operators, && and || have equal precedence, followed by ; and &, which have equal precedence.
> A sequence of one or more newlines may appear in a list instead of a semicolon to delimit commands.
>
> If  a  command  is terminated by the control operator &, the shell executes the command in the background in a subshell.  The shell does not wait for the command to finish, and the return status is 0.  These are referred to as asynchronous commands.  Commands separated by a ; are executed sequentially; the shell waits for  each command to terminate in turn.  The return status is the exit status of the last command executed.
>

> command1 && command2
>
> command2 is executed if, and only if, command1 returns an exit status of zero (success).

`set -e` имеет данное определение:

> When this option is on, if a simple command fails for any of the reasons listed in Consequences of
> Shell Errors or returns an exit status value >0, and is not part of the compound list following a
> while, until, or if keyword, and is not a part of an AND or OR list, and is not a pipeline preceded by
> the ! reserved word, then the shell shall immediately exit.

Следовательно команда при использовании в связке с другими не прервёт их последовательности, а значит, что `&&` и `;` будут иметь равнозначное поведение
