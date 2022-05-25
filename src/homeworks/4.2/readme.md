# Результат выполнения домашнего задания ["4.2. Использование Python для решения типовых DevOps задач"](https://github.com/netology-code/sysadm-homeworks/tree/devsys10/04-script-02-py)

## Обязательная задача 1

Есть скрипт:
```python
#!/usr/bin/env python3
a = 1
b = '2'
c = a + b
```

### Вопросы:
| Вопрос                                          | Ответ                                                                                                                                                            |
| ----------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Какое значение будет присвоено переменной `c`?  | Никакое, будет выброс исключения `TypeError: unsupported operand type(s) for +: 'int' and 'str'`, т.к. мы пытаемся сложить целое число и строку [пример](1-1.py) |
| Как получить для переменной `c` значение 12?    | Нужно перевести `a` в строковое значение `1` через `str(a)` [пример](1-2.py)                                                                                     |
| Как получить для переменной `c` значение 3?     | Нужно задать переменной `b` целочисленное значение через через `int(b)` [пример](1-3.py)                                                                         |

## Обязательная задача 2
Мы устроились на работу в компанию, где раньше уже был DevOps Engineer. Он написал скрипт, позволяющий узнать, какие файлы модифицированы в репозитории, относительно локальных изменений. Этим скриптом недовольно начальство, потому что в его выводе есть не все изменённые файлы, а также непонятен полный путь к директории, где они находятся. Как можно доработать скрипт ниже, чтобы он исполнял требования вашего руководителя?

```python
#!/usr/bin/env python3

import os

bash_command = ["cd ~/netology/sysadm-homeworks", "git status"]
result_os = os.popen(' && '.join(bash_command)).read()
is_change = False
for result in result_os.split('\n'):
    if result.find('modified') != -1:
        prepare_result = result.replace('\tmodified:   ', '')
        print(prepare_result)
        break
```

### Ваш скрипт

[Скрипт](2.py)

Путь до репозитория в скрипте был изменён на актуальный для текущей домашней работы
```python
#!/usr/bin/env python3
import os

project_path = "~/projects/learning/devops-16/"
bash_command = ["cd " + project_path, "git status"]

result_os = os.popen(' && '.join(bash_command)).read()
is_change = False
for result in result_os.split('\n'):
    if result.find('modified') != -1:
        prepare_result = os.path.join(os.path.expanduser(project_path), result.replace('\tmodified:   ', ''))
        is_change = True
        print(prepare_result)
if is_change != True:
    print('No modified files')
```

### Вывод скрипта при запуске при тестировании:
```
./2.py
/home/pavel/projects/learning/devops-16/readme.md
/home/pavel/projects/learning/devops-16/src/homeworks/4.2/1-1.py
/home/pavel/projects/learning/devops-16/src/homeworks/4.2/1-2.py
/home/pavel/projects/learning/devops-16/src/homeworks/4.2/1-3.py
/home/pavel/projects/learning/devops-16/src/homeworks/4.2/2.py
/home/pavel/projects/learning/devops-16/src/homeworks/4.2/readme.md
```

## Обязательная задача 3
Доработать скрипт выше так, чтобы он мог проверять не только локальный репозиторий в текущей директории, а также умел воспринимать путь к репозиторию, который мы передаём как входной параметр. Мы точно знаем, что начальство коварное и будет проверять работу этого скрипта в директориях, которые не являются локальными репозиториями.

### Ваш скрипт:

[Скрипт](3.py)

```python
#!/usr/bin/env python3
import os
import sys
import subprocess

arguments = sys.argv

if len(arguments) <= 1:
    print("Empty path argument")
    exit(1)

if arguments[1].replace(" ", "") == '':
    print("Empty string in path argument")
    exit(1)

project_path = arguments[1]

if os.path.isdir(project_path) != True:
    print("Path is not a directory")
    exit(1)

git_status_command = subprocess.Popen(['git', 'status'], cwd=project_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
git_status_command.wait()

if git_status_command.returncode != 0:
    print("Git repo not found in a directory")
    exit(1)

result_os = git_status_command.stdout.read().decode("utf-8").rstrip()
is_change = False
for result in result_os.split('\n'):
    if result.find('modified') != -1:
        prepare_result = os.path.join(project_path, result.replace('\tmodified:   ', ''))
        is_change = True
        print(prepare_result)
if is_change != True:
    print('No modified files')
```

### Вывод скрипта при запуске при тестировании:
```
./3.py ~/projects/learning/devops-16
/home/pavel/projects/learning/devops-16/src/homeworks/4.2/3.py
/home/pavel/projects/learning/devops-16/src/homeworks/4.2/readme.md
```

## Обязательная задача 4
Наша команда разрабатывает несколько веб-сервисов, доступных по http. Мы точно знаем, что на их стенде нет никакой балансировки, кластеризации, за DNS прячется конкретный IP сервера, где установлен сервис. Проблема в том, что отдел, занимающийся нашей инфраструктурой очень часто меняет нам сервера, поэтому IP меняются примерно раз в неделю, при этом сервисы сохраняют за собой DNS имена. Это бы совсем никого не беспокоило, если бы несколько раз сервера не уезжали в такой сегмент сети нашей компании, который недоступен для разработчиков. Мы хотим написать скрипт, который опрашивает веб-сервисы, получает их IP, выводит информацию в стандартный вывод в виде: <URL сервиса> - <его IP>. Также, должна быть реализована возможность проверки текущего IP сервиса c его IP из предыдущей проверки. Если проверка будет провалена - оповестить об этом в стандартный вывод сообщением: [ERROR] <URL сервиса> IP mismatch: <старый IP> <Новый IP>. Будем считать, что наша разработка реализовала сервисы: `drive.google.com`, `mail.google.com`, `google.com`.

### Ваш скрипт:

[Скрипт](4.py)

```python
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
    time.sleep(10)
```

### Вывод скрипта при запуске при тестировании:
Изменений не ждал, просто в `/etc/hosts` пару раз поменял значения
```
./4.py
drive.google.com - 74.125.205.194
mail.google.com - 216.58.209.197
google.com - 216.58.209.174
[ERROR] drive.google.com IP mismatch: 74.125.205.194 127.0.0.1
mail.google.com - 216.58.209.197
google.com - 216.58.210.142
[ERROR] drive.google.com IP mismatch: 127.0.0.1 74.125.205.194
mail.google.com - 216.58.209.197
google.com - 216.58.210.142
drive.google.com - 74.125.205.194
```