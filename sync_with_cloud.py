import os
import time
import logging

from config_manager import read_config, get_config_value, get_config_int_value
from cloud_storage import YandexDiskClient
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(filename=os.environ.get("LOG_PATH", "./sync.log"), level=logging.INFO, format='%(asctime)s - %(message)s')


def sync_files(local_folder, backup_folder, token, sync_interval):
    yandex_client = YandexDiskClient(token, backup_folder)
    logging.info('Запускаем процесс синхронизации')
    try:
        local_files = {file for file in os.listdir(local_folder) if os.path.isfile(os.path.join(local_folder, file))}
        remote_files_info = yandex_client.get_info()
        remote_files = {item['name'] for item in remote_files_info['items']} if 'items' in remote_files_info else set()

        for file in local_files:
            if file not in remote_files:
                logging.info(f'Загружается новый файл: {file}')
                yandex_client.upload_file(os.path.join(local_folder, file), file)
            else:
                logging.info(f'Обновление файла: {file}')
                yandex_client.upload_file(os.path.join(local_folder, file), file)

        for file in remote_files:
            if file not in local_files:
                logging.info(f'Удаление удаленного файла: {file}')
                yandex_client.delete_file(file)

    except Exception as e:
        logging.error(f'Ошибка во время синхронизации: {str(e)}')


def main():
    config = read_config()
    local_folder = get_config_value(config, 'Settings', 'local_folder')
    backup_folder = get_config_value(config, 'Settings', 'backup_folder')
    token = os.getenv('YANDEX_DISK_TOKEN')
    sync_interval = get_config_int_value(config, 'Settings', 'sync_interval')

    while True:
        sync_files(local_folder, backup_folder, token, sync_interval)
        time.sleep(sync_interval)


if __name__ == '__main__':
    main()
