Результат выполнения домашнего задания ["Инструменты Git"](https://github.com/netology-code/sysadm-homeworks/tree/devsys10/02-git-04-tools)

## Поиск информации по Git

1. Найдите полный хеш и комментарий коммита, хеш которого начинается на `aefea`.

Для поиска информации можно воспользоваться функцией `git show`. Ниже отображён вывод в консоль:
```shell
git --no-pager show -s aefea
commit aefead2207ef7e2aa5dc81a34aedf0cad4c32545
Author: Alisdair McDiarmid <alisdair@users.noreply.github.com>
Date:   Thu Jun 18 10:29:58 2020 -0400

    Update CHANGELOG.md
```
Где `-s` отключает вывод информации о изменениях (`diff`) коммита, а `--no-pager` - отключает вывод в отдельной утилите

Ответ: `aefead2207ef7e2aa5dc81a34aedf0cad4c32545`

2. Какому тегу соответствует коммит `85024d3`?

Для поиска информации воспользуемся функцией из предыдущего пункта, добавив `--oneline`, т.к нам не нужен полный хэш и дополнительная информация:
```shell
git --no-pager show -s --oneline 85024d3     
85024d310 (tag: v0.12.23) v0.12.23
```
Ответ: коммит соответсвует тегу `v0.12.23`

3. Сколько родителей у коммита `b8d720`? Напишите их хеши.

Для поиска информации о родителях можно использовать два способа: через `git log` и `git show`. Оба способа поддерживают форматирование вывода через `--pretty`. Для информации о коммите и родителях требуется задать такой формат вывода `--pretty=format:"commit: %h%nparents: %p%n"`.

В случае использования `git log` команда и вывод будут выглядеть следующим образом:
```shell
git --no-pager log --pretty=format:"commit: %h%nparents: %p%n" -n 1 b8d720
commit: b8d720f83
parents: 56cd7859e 9ea88f22f
```

Для `git show` команда и вывод будут выглядеть следующим образом:
```shell
it --no-pager show --pretty=format:"commit: %h%nparents: %p%n" -s b8d720
commit: b8d720f83
parents: 56cd7859e 9ea88f22f
```
Ответ: у коммита `b8d720` два родителя с хэшами `56cd7859e` и  `9ea88f22f`

4. Перечислите хеши и комментарии всех коммитов которые были сделаны между тегами v0.12.23 и v0.12.24.

Для отображения информации нужно воспользоваться `git log` с указанием нужных тэгов и `..` между ними, для включения коммита, к которому добавлена первая версия, нужно добавить `^` в конце
```shell
git --no-pager log --oneline v0.12.23^..v0.12.24
33ff1c03b (tag: v0.12.24) v0.12.24
b14b74c49 [Website] vmc provider links
3f235065b Update CHANGELOG.md
6ae64e247 registry: Fix panic when server is unreachable
5c619ca1b website: Remove links to the getting started guide's old location
06275647e Update CHANGELOG.md
d5f9411f5 command: Fix bug when using terraform login on Windows
4b6d06cc5 Update CHANGELOG.md
dd01a3507 Update CHANGELOG.md
225466bc3 Cleanup after v0.12.23 release
85024d310 (tag: v0.12.23) v0.12.23
```
Ответ:

| commit    | comment                                                            |
|:----------|:-------------------------------------------------------------------|
| b14b74c49 | [Website] vmc provider links                                       |
| 3f235065b | Update CHANGELOG.md                                                |
| 6ae64e247 | registry: Fix panic when server is unreachable                     |
| 5c619ca1b | website: Remove links to the getting started guide's old location  |
| 06275647e | Update CHANGELOG.md                                                |
| d5f9411f5 | command: Fix bug when using terraform login on Windows             |
| 4b6d06cc5 | Update CHANGELOG.md                                                |
| dd01a3507 | Update CHANGELOG.md                                                |
| 225466bc3 | Cleanup after v0.12.23 release                                     |

5. Найдите коммит в котором была создана функция `func providerSource`, ее определение в коде выглядит так `func providerSource(...)` (вместо троеточия перечислены аргументы).

Поиск коммита можно осуществить по регулярному выражению, для этого воспользуемся флагом `-G` у команды `git log`:
```shell
git --no-pager log --oneline -G"func providerSource(.*)"
f5012c12d command/cliconfig: Installation methods, not installation sources
5af1e6234 main: Honor explicit provider_installation CLI config when present
8c928e835 main: Consult local directories as potential mirrors of providers
```
Нужно быть готовым к тому, что поиск может занять длительное время. Первый коммит, в котором фигурирует искомая функция `8c928e835`

Для проверки того, что это действительно так можно воспользоваться `git show 8c928e835` и увидеть такую строчку в изменениях
```shell
+func providerSource(services *disco.Disco) getproviders.Source {
```
Ответ: коммит `8c928e835`

6. Найдите все коммиты в которых была изменена функция `globalPluginDirs`

Воспользуемся аналогичной 5-му пункту командой:
```shell
git --no-pager log --oneline -G"func globalPluginDirs(.*)"
8364383c3 Push plugin discovery down into command package
```
В выводе видим всего один коммит, само определение функции с момента добавления не менялось

> __Fixed__
>  
> > нужно было найти изменение именно тела функции, а не определения, для этогго можно воспользоваться `git grep`:
> > ```shell
> > git --no-pager grep "globalPluginDirs"             
> > commands.go:		GlobalPluginDirs: globalPluginDirs(),
> > commands.go:	helperPlugins := pluginDiscovery.FindPlugins("credentials", globalPluginDirs())
> > internal/command/cliconfig/config_unix.go:		// FIXME: homeDir gets called from globalPluginDirs during init, before
> > plugins.go:// globalPluginDirs returns directories that should be searched for
> > plugins.go:func globalPluginDirs() []string {
> > ```
> > А после того, как нашли в каком файле фигурирует данная функция `git log -L :globalPluginDirs:plugins.go` и увидеть в выводе работу с телом функции

7. Кто автор функции `synchronizedWriters`?

Воспользуемся командой `git log` изменив при этом форматирование вывода через `--pretty` на `short`

Информация из документации гит о выводе `short`:
```shell
•   short

       commit <hash>
       Author: <author>

       <title line>
```

Результат применения команды с выводом:
```shell
git --no-pager log --pretty=short -G"func synchronizedWriters(.*)"
commit bdfea50cc85161dea41be0fe3381fd98731ff786
Author: James Bardin <j.bardin@gmail.com>

    remove unused

commit 5ac311e2a91e381e2f52234668b49ba670aa0fe5
Author: Martin Atkins <mart@degeneration.co.uk>

    main: synchronize writes to VT100-faker on Windows
```

Ответ: автором функции является `Martin Atkins`