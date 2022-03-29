# Результат выполнения домашнего задания ["3.5. Файловые системы"](https://github.com/netology-code/sysadm-homeworks/tree/devsys10/03-sysadmin-05-fs)

1. Узнайте о [sparse](https://ru.wikipedia.org/wiki/Разрежённый_файл) (разряженных) файлах.

Sparse - файл, в котором последовательности нулевых байтов заменены на информацию об этих последовательностях. Таким образом файл может быть записан разными фрагментами на диске. Это позволит записать большой файл в свободные фрагменты, которые появились, например при удалении другого файла меньшего размера.

2. Могут ли файлы, являющиеся жесткой ссылкой на один объект, иметь разные права доступа и владельца? Почему?

Не могут, т.к. они ссылаются на одну `inode`, которая в свою очередь является явным идентификатором объекта внутри ОС. Поэтому все свойства объектов, ссылающихся на одну `inode` будут идентичны.

3. Новая конфигурация VM

В файл `Vagrantfile` добавлено следующее содержимое с конфигурацией дисков:

```
  config.vm.provider :virtualbox do |vb|
    lvm_experiments_disk0_path = "/tmp/lvm_experiments_disk0.vmdk"
    lvm_experiments_disk1_path = "/tmp/lvm_experiments_disk1.vmdk"
    vb.customize ['createmedium', '--filename', lvm_experiments_disk0_path, '--size', 2560]
    vb.customize ['createmedium', '--filename', lvm_experiments_disk1_path, '--size', 2560]
    vb.customize ['storageattach', :id, '--storagectl', 'SATA Controller', '--port', 1, '--device', 0, '--type', 'hdd', '--medium', lvm_experiments_disk0_path]
    vb.customize ['storageattach', :id, '--storagectl', 'SATA Controller', '--port', 2, '--device', 0, '--type', 'hdd', '--medium', lvm_experiments_disk1_path]
  end
```

После машина переподнята через `vagrant up`. Подключенные диски можно найти через `sudo fdisk -l`:

```
Disk /dev/sdb: 2.51 GiB, 2684354560 bytes, 5242880 sectors
Disk model: VBOX HARDDISK   
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes


Disk /dev/sdc: 2.51 GiB, 2684354560 bytes, 5242880 sectors
Disk model: VBOX HARDDISK   
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
```

4. Используя `fdisk`, разбейте первый диск на 2 раздела: 2 Гб, оставшееся пространство

Утилита `fdisk` интерактивная, значит команды можно выполнять непосредственно после её запуска:

```shell
vagrant@vagrant:/tmp$ sudo fdisk /dev/sdb 

Welcome to fdisk (util-linux 2.34).
Changes will remain in memory only, until you decide to write them.
Be careful before using the write command.

Device does not contain a recognized partition table.
Created a new DOS disklabel with disk identifier 0x2ffe25e0.

Command (m for help): g
Created a new GPT disklabel (GUID: 80E26177-C096-AF45-B47C-BCAEFC29FF01).

Command (m for help): n
Partition number (1-128, default 1): 1
First sector (2048-5242846, default 2048): 2048
Last sector, +/-sectors or +/-size{K,M,G,T,P} (2048-5242846, default 5242846): +2G

Created a new partition 1 of type 'Linux filesystem' and of size 2 GiB.

Command (m for help): n
Partition number (2-128, default 2): 2
First sector (4196352-5242846, default 4196352): 
Last sector, +/-sectors or +/-size{K,M,G,T,P} (4196352-5242846, default 5242846): 

Created a new partition 2 of type 'Linux filesystem' and of size 511 MiB.

Command (m for help): w
The partition table has been altered.
Calling ioctl() to re-read partition table.
Syncing disks.
```

Проверить созданное можно через `sudo fdisk -l`

```
Disk /dev/sdb: 2.51 GiB, 2684354560 bytes, 5242880 sectors
Disk model: VBOX HARDDISK   
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: gpt
Disk identifier: 80E26177-C096-AF45-B47C-BCAEFC29FF01

Device       Start     End Sectors  Size Type
/dev/sdb1     2048 4196351 4194304    2G Linux filesystem
/dev/sdb2  4196352 5242846 1046495  511M Linux filesystem
```
5. Используя sfdisk, перенесите данную таблицу разделов на второй диск

Для переноса воспользуемся документацией и найдём там один из способов переноса через дамп:

```
BACKING UP THE PARTITION TABLE
       It is recommended to save the layout of your devices.  sfdisk supports two ways.

       Use the --dump option to save a description of the device layout to a text file.  The dump format is suitable for later  sfdisk
       input.  For example:

              sfdisk --dump /dev/sda > sda.dump

       This can later be restored by:

              sfdisk /dev/sda < sda.dump
```

Перенесём таблицу разделов с `/dev/sdb` на `/dev/sdc`

```
vagrant@vagrant:/tmp$ sudo sfdisk --dump /dev/sdb > /tmp/sdb.dump

vagrant@vagrant:/tmp$ sudo sfdisk /dev/sdc < sdb.dump 
Checking that no-one is using this disk right now ... OK

Disk /dev/sdc: 2.51 GiB, 2684354560 bytes, 5242880 sectors
Disk model: VBOX HARDDISK   
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes

>>> Script header accepted.
>>> Script header accepted.
>>> Script header accepted.
>>> Script header accepted.
>>> Script header accepted.
>>> Script header accepted.
>>> Created a new GPT disklabel (GUID: 80E26177-C096-AF45-B47C-BCAEFC29FF01).
/dev/sdc1: Created a new partition 1 of type 'Linux filesystem' and of size 2 GiB.
/dev/sdc2: Created a new partition 2 of type 'Linux filesystem' and of size 511 MiB.
/dev/sdc3: Done.

New situation:
Disklabel type: gpt
Disk identifier: 80E26177-C096-AF45-B47C-BCAEFC29FF01

Device       Start     End Sectors  Size Type
/dev/sdc1     2048 4196351 4194304    2G Linux filesystem
/dev/sdc2  4196352 5242846 1046495  511M Linux filesystem

The partition table has been altered.
Calling ioctl() to re-read partition table.
Syncing disks.
```

Проверим перенос `sudo fdisk -l`

```
Disk /dev/sdb: 2.51 GiB, 2684354560 bytes, 5242880 sectors
Disk model: VBOX HARDDISK   
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: gpt
Disk identifier: 80E26177-C096-AF45-B47C-BCAEFC29FF01

Device       Start     End Sectors  Size Type
/dev/sdb1     2048 4196351 4194304    2G Linux filesystem
/dev/sdb2  4196352 5242846 1046495  511M Linux filesystem


Disk /dev/sdc: 2.51 GiB, 2684354560 bytes, 5242880 sectors
Disk model: VBOX HARDDISK   
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: gpt
Disk identifier: 80E26177-C096-AF45-B47C-BCAEFC29FF01

Device       Start     End Sectors  Size Type
/dev/sdc1     2048 4196351 4194304    2G Linux filesystem
/dev/sdc2  4196352 5242846 1046495  511M Linux filesystem
```

6. Соберите `mdadm` RAID1 на паре разделов 2 Гб

Разделы для объединения в RAID1: `/dev/sdb1` и `/dev/sdc1`

```shell
vagrant@vagrant:/tmp$ sudo mdadm --create /dev/md0 --level=1 --raid-devices=2 /dev/sdb1 /dev/sdc1
mdadm: Defaulting to version 1.2 metadata
mdadm: array /dev/md0 started.
```

7. Соберите mdadm RAID0 на второй паре маленьких разделов.

Разделы для объединения в RAID0: `/dev/sdb2` и `/dev/sdc2`

```shell
vagrant@vagrant:/tmp$ sudo mdadm --create /dev/md1 --level=0 --raid-devices=2 /dev/sdb2 /dev/sdc2
mdadm: Defaulting to version 1.2 metadata
mdadm: array /dev/md1 started.
```

8. Создайте 2 независимых PV на получившихся md-устройствах.

```shell
vagrant@vagrant:/tmp$ sudo pvcreate /dev/md0
  Physical volume "/dev/md0" successfully created.
vagrant@vagrant:/tmp$ sudo pvcreate /dev/md1
  Physical volume "/dev/md1" successfully created.
```

Проверим результат через `pvdisplay`

```
  "/dev/md0" is a new physical volume of "<2.00 GiB"
  --- NEW Physical volume ---
  PV Name               /dev/md0
  VG Name               
  PV Size               <2.00 GiB
  Allocatable           NO
  PE Size               0   
  Total PE              0
  Free PE               0
  Allocated PE          0
  PV UUID               FOKuO3-EwXc-hVH0-w2dz-LIi3-CzFU-iSp2RO
   
  "/dev/md1" is a new physical volume of "1017.00 MiB"
  --- NEW Physical volume ---
  PV Name               /dev/md1
  VG Name               
  PV Size               1017.00 MiB
  Allocatable           NO
  PE Size               0   
  Total PE              0
  Free PE               0
  Allocated PE          0
  PV UUID               QkFvRV-jTnE-ybc9-ygBK-okaN-7ed2-VAXiku
```

9. Создайте общую volume-group на этих двух PV.

```shell
vagrant@vagrant:/tmp$ sudo vgcreate test_volume_group /dev/md0 /dev/md1
  Volume group "test_volume_group" successfully created
vagrant@vagrant:/tmp$ sudo vgdisplay
   
  --- Volume group ---
  VG Name               test_volume_group
  System ID             
  Format                lvm2
  Metadata Areas        2
  Metadata Sequence No  1
  VG Access             read/write
  VG Status             resizable
  MAX LV                0
  Cur LV                0
  Open LV               0
  Max PV                0
  Cur PV                2
  Act PV                2
  VG Size               <2.99 GiB
  PE Size               4.00 MiB
  Total PE              765
  Alloc PE / Size       0 / 0   
  Free  PE / Size       765 / <2.99 GiB
  VG UUID               p9hDsq-Jax0-rcGp-KS8p-dDKa-bWdr-ntRcfx
  ```

10. Создайте LV размером 100 Мб, указав его расположение на PV с RAID0

```shell
vagrant@vagrant:/tmp$ sudo lvcreate --size=100MB test_volume_group /dev/md1
  Logical volume "lvol0" created.
vagrant@vagrant:/tmp$ sudo lvdisplay
  --- Logical volume ---
  LV Path                /dev/test_volume_group/lvol0
  LV Name                lvol0
  VG Name                test_volume_group
  LV UUID                PBDtXA-FuEp-7W35-jy2F-p46N-uFrd-2NbBHZ
  LV Write Access        read/write
  LV Creation host, time vagrant, 2022-03-29 16:40:24 +0000
  LV Status              available
  # open                 0
  LV Size                100.00 MiB
  Current LE             25
  Segments               1
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     4096
  Block device           253:1
```

11. Создайте `mkfs.ext4` ФС на получившемся `LV`.

```shell
vagrant@vagrant:/tmp$ sudo mkfs.ext4 /dev/test_volume_group/lvol0
mke2fs 1.45.5 (07-Jan-2020)
Creating filesystem with 25600 4k blocks and 25600 inodes

Allocating group tables: done                            
Writing inode tables: done                            
Creating journal (1024 blocks): done
Writing superblocks and filesystem accounting information: done
```

12. Смонтируйте этот раздел в любую директорию, например, `/tmp/new`.

```shell
vagrant@vagrant:/tmp$ mkdir /tmp/new
vagrant@vagrant:/tmp$ sudo mount /dev/test_volume_group/lvol0 /tmp/new/
```

13. Поместите туда тестовый файл, например `wget https://mirror.yandex.ru/ubuntu/ls-lR.gz -O /tmp/new/test.gz`

```shell
vagrant@vagrant:/tmp$ sudo wget https://mirror.yandex.ru/ubuntu/ls-lR.gz -O /tmp/new/test.gz
--2022-03-29 16:44:06--  https://mirror.yandex.ru/ubuntu/ls-lR.gz
Resolving mirror.yandex.ru (mirror.yandex.ru)... 213.180.204.183, 2a02:6b8::183
Connecting to mirror.yandex.ru (mirror.yandex.ru)|213.180.204.183|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 22465261 (21M) [application/octet-stream]
Saving to: ‘/tmp/new/test.gz’

/tmp/new/test.gz                   100%[==============================================================>]  21.42M  2.95MB/s    in 7.4s    

2022-03-29 16:44:14 (2.90 MB/s) - ‘/tmp/new/test.gz’ saved [22465261/22465261]
```

14. Прикрепите вывод `lsblk`.

```shell
vagrant@vagrant:/tmp$ sudo lsblk
NAME                          MAJ:MIN RM  SIZE RO TYPE  MOUNTPOINT
loop0                           7:0    0 55.4M  1 loop  /snap/core18/2128
loop2                           7:2    0 70.3M  1 loop  /snap/lxd/21029
loop3                           7:3    0 43.6M  1 loop  /snap/snapd/15177
loop4                           7:4    0 55.5M  1 loop  /snap/core18/2344
loop5                           7:5    0 61.9M  1 loop  /snap/core20/1405
loop6                           7:6    0 67.8M  1 loop  /snap/lxd/22753
sda                             8:0    0   64G  0 disk  
├─sda1                          8:1    0    1M  0 part  
├─sda2                          8:2    0    1G  0 part  /boot
└─sda3                          8:3    0   63G  0 part  
  └─ubuntu--vg-ubuntu--lv     253:0    0 31.5G  0 lvm   /
sdb                             8:16   0  2.5G  0 disk  
├─sdb1                          8:17   0    2G  0 part  
│ └─md0                         9:0    0    2G  0 raid1 
└─sdb2                          8:18   0  511M  0 part  
  └─md1                         9:1    0 1017M  0 raid0 
    └─test_volume_group-lvol0 253:1    0  100M  0 lvm   /tmp/new
sdc                             8:32   0  2.5G  0 disk  
├─sdc1                          8:33   0    2G  0 part  
│ └─md0                         9:0    0    2G  0 raid1 
└─sdc2                          8:34   0  511M  0 part  
  └─md1                         9:1    0 1017M  0 raid0 
    └─test_volume_group-lvol0 253:1    0  100M  0 lvm   /tmp/new
```

15. Протестируйте целостность файла

```shell
vagrant@vagrant:/tmp$ gzip -t /tmp/new/test.gz
vagrant@vagrant:/tmp$ echo $?
0
```

16. Используя `pvmove`, переместите содержимое `PV` с `RAID0` на `RAID1`.

```shell
vagrant@vagrant:/tmp$ sudo pvmove /dev/md1 /dev/md0
  /dev/md1: Moved: 16.00%
  /dev/md1: Moved: 100.00%
```

17. Сделайте `--fail` на устройство в вашем `RAID1` md.

```shell
vagrant@vagrant:/tmp$ sudo mdadm --fail /dev/md0 /dev/sdb1
mdadm: set /dev/sdb1 faulty in /dev/md0
```

18. Подтвердите выводом `dmesg`, что `RAID1` работает в деградированном состоянии.

```shell
vagrant@vagrant:/tmp$ dmesg | tail -n 10
[ 1408.087732] md/raid1:md0: not clean -- starting background reconstruction
[ 1408.087734] md/raid1:md0: active with 2 out of 2 mirrors
[ 1408.087754] md0: detected capacity change from 0 to 2144337920
[ 1408.088269] md: resync of RAID array md0
[ 1418.320646] md: md0: resync done.
[ 1457.759721] md1: detected capacity change from 0 to 1066401792
[ 2086.804298] EXT4-fs (dm-1): mounted filesystem with ordered data mode. Opts: (null)
[ 2086.804309] ext4 filesystem being mounted at /tmp/new supports timestamps until 2038 (0x7fffffff)
[ 2480.759016] md/raid1:md0: Disk failure on sdb1, disabling device.
               md/raid1:md0: Operation continuing on 1 devices.
```

19. Протестируйте целостность файла, несмотря на "сбойный" диск он должен продолжать быть доступен:

```shell
vagrant@vagrant:/tmp$ gzip -t /tmp/new/test.gz
vagrant@vagrant:/tmp$ echo $?
0
```
