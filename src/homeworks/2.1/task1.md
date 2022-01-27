Создана директория [src/terraform](/src/terraform). Добавлен файл [src/terraform/.gitignore](/src/terraform/.gitignore)

Файлы, которые будут проигнорированы git'ом:

* Любые файлы в директории `.terraform`, в любом месте глубже, независимо от глубины
* Файлы с расширением `.tfstate` или имеющие в названии `.tfstate.`
* Файлы с названием `crash.log`
* Файлы с расширением `.log` и начинающиеся с `crash.`
* Файлы с расширением `.tfvars`
* Файлы с названиями `override.rf` и `override.tf.json`
* Файлы с названиями, оканчивающимися на `_override.tf` и `_override.tf.json`
* Файлы с названиями `.terraformrc` и `terraform.rc`
