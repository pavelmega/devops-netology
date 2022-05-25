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
| Как получить для переменной `c` значение 12?    | Нужно задать переменной `a` строковое значение `1` аналогично переменной `b` [пример](1-2.py)                                                                    |
| Как получить для переменной `c` значение 3?     | Нужно задать переменной `b` целочисленное значение, просто убрав кавычки  [пример](1-3.py)                                                                       |

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
        prepare_result = project_path + result.replace('\tmodified:   ', '')
        prepare_result = os.path.join(project_path, result.replace('\tmodified:   ', ''))
        is_change = True
        print(prepare_result)
if is_change != True:
    print('No modified files')
```

### Вывод скрипта при запуске при тестировании:
```
./2.py
~/projects/learning/devops-16/readme.md
~/projects/learning/devops-16/src/homeworks/4.2/1-1.py
~/projects/learning/devops-16/src/homeworks/4.2/1-2.py
~/projects/learning/devops-16/src/homeworks/4.2/1-3.py
~/projects/learning/devops-16/src/homeworks/4.2/2.py
```
