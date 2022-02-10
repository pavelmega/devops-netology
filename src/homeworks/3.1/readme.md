Результат выполнения домашнего задания ["Работа в терминале, лекция 1"](https://github.com/netology-code/sysadm-homeworks/tree/devsys10/03-sysadmin-01-terminal)

## Vagrant

1. Какие ресурсы выделены по-умолчанию для машины, которую создал Vagrant?

    Ответ:
    ```
    CPU: 2
    RAM: 1024 MB
    VRAM: 4 MB
    Storage: 64 GB
    ```

2. Как добавить оперативной памяти или ресурсов процессора виртуальной машине?

    Ответ: В конфигурационный файл `Vagrantfile` необходимо добавить следующие строки (количество ресурсов можно указать другое):
    ```
    config.vm.provider "virtualbox" do |v|
      v.memory = 2048
      v.cpus = 4
    end
    ```
   
## man bash

1. Какой переменной можно задать длину журнала `history`, и на какой строчке manual это описывается:

    Ответ: Переменная `HISTSIZE`
    
    Для того, чтобы узнать строку, можно посмотреть в нижнюю часть терминала с открытым мануалом,
    там отображается номер текущей (самой верхней) строки. Нужно учитывать то, что строки нумеруются относительно вывода
    мануала на экран терминала, если использовать разные размеры терминала по количеству символов, например просто развенув
    его на весь экран, номера строк будут разные (при изменении размера терминала придется переоткрыть мануал, иначе
    не произойдёт повторного рендера).
    
    Пример отображения номера строки:
    ```
    Manual page bash(1) line 1 (press h for help or q to quit)
    ```
    Также для этображения номеров строк на дисплее можно воспользоваться кастомным пейджером:
    ```
    Controlling formatted output
           -P pager, --pager=pager
    ```
    Например, в качестве пейджера можно использовать `less`, в мануале которого можно найти вывод строк:
    ```
    -N or --LINE-NUMBERS
          Causes a line number to be displayed at the beginning of each line in the display.
    ```
    В конечном виде команда для запуска отображения мануала к `bash` будет выглядеть следующим образом:
    ```
    man -P "less -N" bash
    ```
    Для терминала на моей машине описание переменной `HISTSIZE` начинается на строке 581
    
    ```
    581        HISTSIZE
    582               The  number  of  commands  to remember in the command history (see HISTORY below).  If the value    582  is 0, commands are not saved in the history list.  Numeric values less than zero result in every command bein    582 g saved on the history list
    ```
   
2. что делает директива `ignoreboth` в bash?

   `ignoreboth` выступает в качестве значения для переменной `HISTCONTROL` и является простым сокращением для
   `ignorespace` и `ignoredups`, а значит и включает одновременно действия обеих:
   - `ignorespace` - если команда начинается с пробела, она не будет сохраняться в истории
   - `ignoredups` - если команда совпадает с предыдущей записью в истории, она не будет сохранена

3. В каких сценариях использования применимы скобки `{}` и на какой строчке `man bash` это описано?

    Ответ: данный вид скобок применим в составных командах `Compound Commands`, их описание начинается на 186 строке мануала
    ```
    186    Compound Commands
    187        A compound command is one of the following.  In most cases a list in a command's description may be separated from the rest of the command by one or more newlines, and may be followed by a newline in place of a semicolon.
    ```

4. С учётом ответа на предыдущий вопрос, как создать однократным вызовом `touch` 100000 файлов?
Получится ли аналогичным образом создать 300000? Если нет, то почему?

    Ответ: команда для создания 100000 файлов будет выглядеть следующим образом:
    ```
    touch {1..100000}
    ```
    Создать 300000 аналогичным образом не выйдет, мы получим ошибку вида:
    ```shell
    touch {1..300000}
    -bash: /usr/bin/touch: Argument list too long
    
    ```
    Связано это с ограничением на количество аргументов. Максимальное значение хранится
    в переменной `ARG_MAX` для данной системы оно равно 2097152:
    ```shell
    vagrant@vagrant:~$ getconf ARG_MAX
    2097152
    ```

5. Что делает конструкция `[[ -d /tmp ]]`

    Ответ: использование `[[]]`, позволяет выполнять комады с проверкой на условия.
    
    Команда выше, с указанием `-d`: 
    ```
    -d file
          True if file exists and is a directory.
    ```
    вернёт 0 если  `/tmp` существует и это директория и 1 в ином случае:
    
    ```shell
    vagrant@vagrant:~$ [[ -d /tmp ]]
    vagrant@vagrant:~$ echo $?
    0
    ```
    ```shell
    vagrant@vagrant:~$ [[ -d /tmp/test ]]
    vagrant@vagrant:~$ echo $?
    1
    ```
    также проверка содержится в [conditional_expression.sh](./conditional_expresion.sh)

6. Основываясь на знаниях о просмотре текущих (например, PATH) и установке новых переменных; командах,
которые мы рассматривали, добейтесь в выводе type -a bash в виртуальной машине наличия первым пунктом в списке:

    ```shell
    bash is /tmp/new_path_directory/bash
    bash is /usr/local/bin/bash
    bash is /bin/bash
    ```
      
    Ответ: этого можно добиться создав новую директорию, сделав симлинк в ней на текущий `bash`
и добавив новый путь в переменную `PATH`:

    Создаём новую диреректорию через:
    ```shell
    vagrant@vagrant:~$ mkdir /tmp/new_path_directory/
    ```
    Делаем символическую ссылку на текущий `bash`:
    ```shell
    vagrant@vagrant:~$ ln -s /usr/bin/bash /tmp/new_path_directory/bash
    ```
    Добавляем новый путь к `bash` в переменную `PATH`:
    ```shell
    vagrant@vagrant:~$ export PATH=/tmp/new_path_directory:$PATH
    ```
    Проверяем результат:
    ```shell
    vagrant@vagrant:~$ type -a bash
    bash is /tmp/new_path_directory/bash
    bash is /usr/bin/bash
    bash is /bin/bash
    ```

7. Чем отличается планирование команд с помощью `batch` и `at`?

   Ответ: Планинирование не отличается, у этих команд один мануал. Отличается само применение этих команд.
   * `at` - выполняет команды в определённое время `at      executes commands at a specified time`:
   * `batch` - выполняет команды когда позволяет нагрузка `batch   executes commands when system load levels permit`
