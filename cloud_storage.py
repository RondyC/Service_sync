import yadisk
import os
import logging


class YandexDiskClient:
    def __init__(self, token):
        self.ya_disk = yadisk.YaDisk(token=token)

        if not self.ya_disk.check_token():
            logging.error('Токен Яндекс Диска недействителен.')
            raise ValueError('Неверный токен')

    def upload_file(self, local_path, remote_filename=None):
        if not remote_filename:
            remote_filename = os.path.basename(local_path)

        self.ya_disk.upload(local_path, remote_filename)
        logging.info(f'Загружено {local_path} в облако')

    def get_info(self, folder):
        try:
            files_info = list(self.ya_disk.listdir(folder))  # Преобразуем генератор в список
            print("Files info:", files_info)  # Отладочный вывод
            return {item['name']: item for item in files_info}
        except yadisk.exceptions.PathNotFoundError:
            logging.error(f'Ошибка при получении информации о файлах: Не удалось найти запрошенный ресурс.')
            return {}

    def update_file(self, local_path, remote_path):
        self.ya_disk.upload(local_path, remote_path, overwrite=True)  # Перезаписываем файл
        logging.info(f'Обновлен файл {remote_path} в облаке')

    def delete_file(self, file_name):
        try:
            if self.ya_disk.exists(file_name):  # Проверяем существование файла на диске
                self.ya_disk.remove(file_name)
                logging.info(f'Удалено {file_name} из облака')
            else:
                logging.info(f'Файл {file_name} не существует на облаке')
        except Exception as e:
            logging.error(f'Ошибка при удалении файла {file_name} из облака: {str(e)}')
