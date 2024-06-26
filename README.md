[![Python](https://img.shields.io/badge/-Python-464646?style=flat&logo=Python&logoColor=ffffff&color=043A6B)](https://www.python.org/)
[![BeautifulSoup4](https://img.shields.io/badge/-BeautifulSoup4-464646?style=flat&logo=BeautifulSoup4&logoColor=ffffff&color=043A6B)](https://www.crummy.com/software/BeautifulSoup/)
[![Prettytable](https://img.shields.io/badge/-Prettytable-464646?style=flat&logo=Prettytable&logoColor=ffffff&color=043A6B)](https://github.com/jazzband/prettytable)
[![Logging](https://img.shields.io/badge/-Logging-464646?style=flat&logo=Logging&logoColor=ffffff&color=043A6B)](https://docs.python.org/3/library/logging.html)

### Парсер сайтов по документации Python и стандартам PEP

## Описание

Учебный проект для практики создания парсеров.

Парсится документация Python: PEP, версии, обновления, архив с документацией.

В проекте реализован парсинг аргументов командной строки для выбора режима работы программы. Всего доступно четыре режима:
- **whats-new** (получение списка ссылок на перечень изменений в версиях Python)
- **latest-versions** (получение списка ссылок на документацию для всех версий Python)
- **download** (скачивание архива с документацией для последней версии Python)
- **pep** (получение данных о статусах всех PEP и вывод информации о несоответствиях статусов в общем списке и в карточках отдельных PEP)

Реализована возможность выбора формата вывода:
- стандартный вывод в терминал;
- вывод в терминал в табличной форме (prettytable);
- запись результатов работы в файл .csv.

Настроено логирование - логи выводятся в терминал и сохраняются в отдельной директории с ротацией.

Список поддерживаемых сайтов:

- https://docs.python.org/3/

- https://peps.python.org/

## Ключевые технологии и библиотеки:
- [Python](https://www.python.org/);
- [BeautifulSoup](https://pypi.org/project/beautifulsoup4/);
- [requests_cache](https://pypi.org/project/requests-cache/);
- [argparse](https://docs.python.org/3/library/argparse.html);
- [prettytable](https://pypi.org/project/prettytable/);
- [tqdm](https://pypi.org/project/tqdm/).

### Инструкция по запуску:
**Клонируйте репозиторий:**
```
git clone git@github.com:babichdenis/bs4_parser_pep.git
```

**Установите и активируйте виртуальное окружение:**

для MacOS:
```
python3 -m venv venv
source venv/bin/activate
```

для Windows:
```
python -m venv venv
source venv/Scripts/activate
```
**Установите зависимости из файла requirements.txt:**
```
pip install -r requirements.txt
```

**Перейдите в папку "src":**
```
cd src
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

### Автор проекта:

[babichdenis](https://github.com/babichdenis/)