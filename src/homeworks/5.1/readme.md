# Результат выполнения домашнего задания ["5.1 Введение в виртуализацию"](https://github.com/netology-code/virt-homeworks/tree/virt-11/05-virt-01-basics)

## Задача 1

> Опишите кратко, как вы поняли: в чем основное отличие полной (аппаратной) виртуализации, паравиртуализации и виртуализации на основе ОС.

1. Паравиртуализация - виртуализация, для работы которой используется прослойка в виде гипервизора, имеющая API для работы с гостеовой ОС и при этом взаимодействует с аппаратной частью через ядро операционной системы хоста. Гипервизор модифицирует ядро гостевой ОС.
2. Полная (аппаратная) - реализуется через инструкции в самом центральном процессоре, что позволяет отказаться от хостовой операционной системы и напрямую обращаться к аппаратным ресурсам.
3. Виртуализация уровня ОС - реализуется взаимодействием через ядро хостовой ОС

## Задача 2
> Выберите один из вариантов использования организации физических серверов, в зависимости от условий использования.
>
> Организация серверов:
> * физические сервера,
> * паравиртуализация,
> * виртуализация уровня ОС.
>
> Условия использования:
> * Высоконагруженная база данных, чувствительная к отказу.
> * Различные web-приложения.
> * Windows системы для использования бухгалтерским отделом.
> * Системы, выполняющие высокопроизводительные расчеты на GPU.
> 
> Опишите, почему вы выбрали к каждому целевому использованию такую организацию.

1. Высоконагруженная база данных, чувствительная к отказу.

Лучше использовать физические сервера, чтобы снизить потери на виртуализацию, любая виртуализация несёт накладные расходы на взаимодействие между системами. Для высоконагруженных систем - это довольно критичный показатель.

2. Различные web-приложения.

В данном случае лучше использовать виртуализацию уровня ОС. Это позволит запускать любые приложения в одинаковом окружении, независимо от того на какой физической машине мы это разворачиваем. Также процессы каждого приложения будут изолированы друг от друга для безопасности.

3. Windows системы для использования бухгалтерским отделом.

В этом случае лучше всего использовать паравиртуализацию. Операционные системы в этом случае одинаковые. Такая реализация позволит уменьшить потери в скорости взаимодействия пользователей с системой.

4. Системы, выполняющие высокопроизводительные расчеты на GPU.

В данном варианте лучше использовать физические сервера, т.к. само железо GPU имеет особую архитектуру, которую не очень просто виртуализировать. К этому ещё добавятся просадки в производительности из-за виртуализации, накладные расходы на гипервизора.

## Задача 3

> Выберите подходящую систему управления виртуализацией для предложенного сценария. Детально опишите ваш выбор.

1. 100 виртуальных машин на базе Linux и Windows, общие задачи, нет особых требований. Преимущественно Windows based инфраструктура, требуется реализация программных балансировщиков нагрузки, репликации данных и автоматизированного механизма создания резервных копий.

Для данной задачи подходящей системой будет `Microsoft Hyper-V`. Обосновано это несколькими параметрами: 
* `Преимущественно Windows based инфраструктура` - `Hyper-V` имеет нативную поддержку данной ОС, но также позволяет работать и с системами на базе Linux
* Сразу имеет возможность работы с репликацией и миграцией данных, соответвенно не должно быть проблем с балансировкой и резервным копированием

2. Требуется наиболее производительное бесплатное open source решение для виртуализации небольшой (20-30 серверов) инфраструктуры на базе Linux и Windows виртуальных машин.

Из бесплатных решений лучше всего подойдёт `Xen`:
* Поддерживает гостевые системы как `Windows`, так и `Linux`
* Имеет высокую производительность
* В отличие от `KVM` сразу выделяет ресурсы и использует их не оказывая влияния на производительность соседних виртуальных машин. 

3. Необходимо бесплатное, максимально совместимое и производительное решение для виртуализации Windows инфраструктуры.

В данном варианте лучшим решением будет `Microsoft Hyper-V Server`:
* Имеет нативную поддержку систем `Windows`, для этого и разрабатывался. А значит имеет и максимальную совместимость и производительность для данного типа систем.
* Является бесплатной ОС

4. Необходимо рабочее окружение для тестирования программного продукта на нескольких дистрибутивах Linux.

Тут выбор можно остановить на `KVS`:
* Позволяет использовать шаблоны виртуальных машин для быстрого поднятия стендов независимо от целей использования (разработка, тестирование)
* Имеет высокую производительность, близкую к нативной
* Нативная для большинства ядер `Linux`

## Задача 4

> Опишите возможные проблемы и недостатки гетерогенной среды виртуализации (использования нескольких систем управления виртуализацией одновременно) и что необходимо сделать для минимизации этих рисков и проблем.

* Поддержка нескольких систем требует дополнительных расходов на специалистов. Это или нужны отдельные инженеры или повышать компетенции текущих
* Возможны проблемы с перемещением данных внутри виртуальных машин управляемых разными гипервизорами
* При использовании любых решений, не только в виртуализации, нужно максимально придерживаться подхода стандартизации как к процессам, так и к применяемым технологиям

> Если бы у вас был выбор, то создавали бы вы гетерогенную среду или нет? Мотивируйте ваш ответ примерами.

Для выбора какого-либо инструмента виртуализации и построения инфраструктуры нужно:
- Определиться с решаемой задачей и тем какие системы мы собираемся поддерживать
- Какие есть требования к инфраструктуре
- Провести анализ рынка вендоров продуктов виртуализации
- Изучить компетенции своего штата инженеров
- Изучить рынок вакансий, определить насколько то или иное решение сейчас находится "в тренде"
- Определить требования к безопасности

Без изучения текущих вопросов однозначно ответить за создание или против гетерогенной среды невозможно.