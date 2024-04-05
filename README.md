# Проект "Синхронизация файлов с облачным хранилищем"

Этот проект представляет собой программу для синхронизации файлов на компьютере пользователя с облачным хранилищем файлов (в данном случае, Яндекс.Диском).

## Описание

Программа обеспечивает синхронизацию файлов между указанной директорией на компьютере пользователя и облачным хранилищем на Яндекс.Диске. Она отслеживает изменения в файлах на компьютере пользователя и автоматически выполняет соответствующие действия (загрузка, обновление, удаление) на Яндекс.Диске при появлении, изменении или удалении файлов.

## Как запустить

1. **Установите необходимые зависимости**: выполните команду `pip install -r requirements.txt` для установки всех необходимых библиотек.
2. **Укажите токен доступа к Яндекс.Диску**: создайте файл `.env` в корневой директории проекта и добавьте туда свой токен доступа в формате `YANDEX_DISK_TOKEN=ваш_токен_здесь`.
3. **Настройте файл конфигурации**: отредактируйте файл `config.ini`, указав путь к синхронизируемой папке, имя папки в облачном хранилище и другие настройки.
4. **Запустите программу**: выполните команду `python sync_with_cloud.py` для запуска программы.

## Примеры ввода и вывода

### Пример 1: Загрузка нового файла в облако

**Ввод:**
Создаём новый файл test.txt в локальной папке ./test

**Вывод (лог программы):**
Загружается новый файл: test.txt
Uploaded ./test/test.txt to cloud

### Пример 2: Обновление файла в облаке

**Ввод:**
Изменяем файл test.txt в локальной папке ./test

**Вывод (лог программы):**
Обновление файла: test.txt
Updating ./test/test.txt to cloud


### Пример 3: Удаление файла из облака

**Ввод:**
Удаляем файл test.txt из локальной папки ./test


**Вывод (лог программы):**
Удаление удаленного файла: test.txt
Deleted test.txt from cloud




