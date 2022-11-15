# Результат выполнения домашнего задания ["5.2 Применение принципов IaaC в работе с виртуальными машинами"](https://github.com/netology-code/virt-homeworks/tree/virt-11/05-virt-02-iaac)

## Задача 1
> * Опишите своими словами основные преимущества применения на практике IaaC паттернов.

Основные преимущества IaaC паттернов:
1. Вся конфигурация хранится под системой контроля версий, осюда выходит несколько преимуществ:
    1. Версионирования, что позволяет производить сравнение версий, проводить ревью множеством инженеров
    2. Единая точка хранения конфигураций
    3. Совместная разработка нескольких инженеров над разными блоками(модулями) конфигурации
2. Возможность легко прочитать конфигурацию, чтобы понять как она работает
3. Воможность автоматизации применения конфигурации к инфраструктуре
4. Возможность оттестировать конфигурацию на различных стендах до выкатки на бой

> * Какой из принципов IaaC является основополагающим?

Основополагающий принцип - идемпотентность. Иными словами он значит то, что применяя одну конфигурацию бесконечное множество раз результат должен быть всегда ожидаем и одинаков.

## Задача 2

> Чем Ansible выгодно отличается от других систем управление конфигурациями?

Самое главное выгодное отличие `ansible` - в том, что его установка необходима только на машине, с которой будет выполняться запуск применения конфигурации. На машинах, на которых требуется выполнить конфигурирование никакого дополнительного софта не требуется, всё взаимодействие осуществляется через `ssh`.

> Какой, на ваш взгляд, метод работы систем конфигурации более надёжный push или pull?

`push` - надёжней, т.к. работает по принципу отправки обновленной конфигурации на машины, дополнительно не нужно держать какой-то фоновый процесс для отдачи обновлённой конфигурации по запросу клиента.

## Задача 3

> Установить на личный компьютер:
> * VirtualBox 
> * Vagrant 
> * Ansible 
> 
> Приложить вывод команд установленных версий каждой из программ, оформленный в markdown.

```shell
virtualbox --help
Oracle VM VirtualBox VM Selector v6.1.32
(C) 2005-2022 Oracle Corporation
All rights reserved.

No special options.

If you are looking for --startvm and related options, you need to use VirtualBoxVM.
```

```shell
vagrant --version
Vagrant 2.2.19
```

```shell
ansible --version
ansible 2.9.6
  config file = /etc/ansible/ansible.cfg
  configured module search path = ['/home/pavel/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/lib/python3/dist-packages/ansible
  executable location = /usr/bin/ansible
  python version = 3.8.10 (default, Jun 22 2022, 20:18:18) [GCC 9.4.0]

```
## Задача 4 (*)

>Воспроизвести практическую часть лекции самостоятельно.
>
> * Создать виртуальную машину.
> * Зайти внутрь ВМ, убедиться, что Docker установлен с помощью команды
> ```
> docker ps
> ```

Для разворачивания использован `Vagrantfile` из прошлого домашнего задания 3.1. В него добавлен блок установки `Docker`

```
  config.vm.provision "shell", inline: <<-SHELL
    apt update
    apt install -y ca-certificates \
        curl \
        gnupg \
        lsb-release
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
        $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
    apt update
    apt install -y docker-ce docker-ce-cli containerd.io
    usermod -aG docker vagrant
  SHELL
```

Проверить установку можно зайдя на виртуальную машину и запустив команду `docker ps`

```shell
vagrant ssh    
Welcome to Ubuntu 20.04.3 LTS (GNU/Linux 5.4.0-91-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Tue 15 Nov 2022 03:32:02 PM UTC

  System load:  1.06               Processes:                126
  Usage of /:   12.6% of 30.88GB   Users logged in:          0
  Memory usage: 24%                IPv4 address for docker0: 172.17.0.1
  Swap usage:   0%                 IPv4 address for eth0:    10.0.2.15


This system is built by the Bento project by Chef Software
More information can be found at https://github.com/chef/bento
vagrant@vagrant:~$ docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```