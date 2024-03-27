<a href="https://codeclimate.com/github/babichdenis/bs4_parser_pep/maintainability"><img src="https://api.codeclimate.com/v1/badges/f662db790b579c11319b/maintainability" /></a>
[![Python](https://img.shields.io/badge/-Python-464646?style=flat&logo=Python&logoColor=ffffff&color=043A6B)](https://www.python.org/)
[![BeautifulSoup4](https://img.shields.io/badge/-BeautifulSoup4-464646?style=flat&logo=BeautifulSoup4&logoColor=ffffff&color=043A6B)](https://www.crummy.com/software/BeautifulSoup/)
[![Prettytable](https://img.shields.io/badge/-Prettytable-464646?style=flat&logo=Prettytable&logoColor=ffffff&color=043A6B)](https://github.com/jazzband/prettytable)
[![Logging](https://img.shields.io/badge/-Logging-464646?style=flat&logo=Logging&logoColor=ffffff&color=043A6B)](https://docs.python.org/3/library/logging.html)

### Парсер сайтов по документации Python и стандартам PEP

### Описание:
Парсер выполняет сбор информации об актуальных версиях документации Python и стандартах PEP, отображая результаты парсинга в нескольких форматах на выбор.

Список поддерживаемых сайтов:

- https://docs.python.org/3/

- https://peps.python.org/

### Инструкция по запуску:
**Клонируйте репозиторий:**
```
git clone git@github.com:VadimVolkovsky/bs4_parser_pep.git
```

**Установите и активируйте виртуальное окружение:**
для MacOS:
```
python3 -m venv venv
```

для Windows:
```
python -m venv venv
source venv/bin/activate
source venv/Scripts/activate
```
**Установите зависимости из файла requirements.txt:**
```
pip install -r requirements.txt
```

**Перейдите в папку "src":**
```
cd src/
```

**Запустите парсер в одном из режимов:**

```
python main.py <parser_mode> <args>
```

### Режимы парсера:
При запуске парсера необходимо выбрать один из режимов <parser_mode>:

+ **whats-new**

Парсинг последних обновлений с сайта
```
python main.py whats-new <args>
```

+ **latest-versions**

Парсинг последних версий документации
```
python main.py latest_versions <args>
```

+ **download**

Загрузка и сохранение архива с документацией
```
python main.py download <args>
```

+ **pep**

Парсинг статусов PEP
```
python main.py pep <args>
```

### Аргументы парсера:
**При запуске парсера можно указать дополнительные аргументы <args>:**

+ **Вывести информацию о парсере:**
```
python main.py <parser_mode> -h
python main.py <parser_mode> --help
```

+ **Очистить кеш:**
```
python main.py <parser_mode> -c
python main.py <parser_mode> --clear-cache
```

+ **Настроить режим отображения результатов:**

Сохранение результатов в CSV файл:
```
python main.py <parser_mode> --output file
```
Отображение результатов в табличном формате в консоли:
```
python main.py <parser_mode> --output pretty
```

Если не указывать аргумент --output, результат парсинга будет выведен в консоль:
  
(кроме парсера download)
```
python main.py <parser_mode>
```

**Технологии:**
- Python 3.9
- BeautifulSoup4

### Автор проекта:


babichdenis