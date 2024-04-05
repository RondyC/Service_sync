import os
import time
import logging

from config_manager import read_config, get_config_value, get_config_int_value
from cloud_storage import YandexDiskClient
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(filename=os.environ.get("LOG_PATH", "./sync.log"), level=logging.INFO, format='%(asctime)s - %(message)s')


def sync_files(local_folder, yandex_client, backup_folder):
    logging.info('Запускаем процесс синхронизации')
    try:
        # Список локальных файлов
        local_files = {file: os.path.getmtime(os.path.join(local_folder, file)) for file in os.listdir(local_folder) if
                       os.path.isfile(os.path.join(local_folder, file))}
        print("Local files:", local_files)  # Отладочный вывод

        # Получаем список файлов на Яндекс.Диске
        remote_files_info = yandex_client.get_info(backup_folder)
        remote_files = {item['name']: item for item in remote_files_info.values()}
        print("Remote files:", remote_files)  # Отладочный вывод

        # Загрузка и обновление файлов
        for local_file, local_mtime in local_files.items():
            local_file_path = os.path.join(local_folder, local_file).replace('\\', '/')
            print(f'Пытаемся загрузить файл: {local_file_path}')  # Отладочный вывод
            if local_file in remote_files:
                remote_file_path = remote_files[local_file]['path']
                logging.info(f'Обновляем файл: {local_file}')
                yandex_client.update_file(local_file_path, remote_file_path)  # Обновляем существующий файл
            else:
                if backup_folder == '':  # Проверяем, что backup_folder пустая строка
                    print(f'Загружаем файл: {local_file_path}')
                    logging.info(f'Загружаем новый файл: {local_file}')
                    yandex_client.upload_file(local_file_path, backup_folder)  # Загружаем новый файл

        # Удаление отсутствующих файлов на Яндекс.Диске
        for remote_file in remote_files.keys():
            if remote_file not in local_files:
                logging.info(f'Удаляем файл с Яндекс.Диска: {remote_file}')
                yandex_client.delete_file(remote_files[remote_file]['path'])

    except Exception as e:
        logging.error(f'Ошибка во время синхронизации: {e}')


def main():
    config = read_config()
    local_folder = get_config_value(config, 'Settings', 'local_folder')
    backup_folder_name = ''  # Пустая строка означает корень диска
    token = os.getenv('YANDEX_DISK_TOKEN')
    sync_interval = get_config_int_value(config, 'Settings', 'sync_interval')

    yandex_client = YandexDiskClient(token)

    while True:
        sync_files(local_folder, yandex_client, backup_folder_name)
        time.sleep(sync_interval)


if __name__ == '__main__':
    main()
