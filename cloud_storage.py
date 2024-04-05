from builtins import ValueError

import yadisk
import os
import logging


class YandexDiskClient:
    def __init__(self, token, backup_folder):
        self.ya_disk = yadisk.YaDisk(token=token)
        self.backup_folder = backup_folder

        if not self.ya_disk.check_token():
            logging.error('Токен Яндекс Диска недействителен.')
            raise ValueError('Неверный токен')
        if not self.ya_disk.exists(self.backup_folder):
            self.ya_disk.mkdir(self.backup_folder)
            logging.info(f'Создана папка в облаке: {self.backup_folder}')

    def upload_file(self, local_path, remote_filename=None):
        if not remote_filename:
            remote_filename = os.path.basename(local_path)
        remote_path = os.path.join(self.backup_folder, remote_filename)
        self.ya_disk.upload(local_path, remote_path)
        logging.info(f'Загружено {local_path} в облако')

    def delete_file(self, file_name):
        remote_path = os.path.join(self.backup_folder, file_name)
        self.ya_disk.remove(remote_path)
        logging.info(f'Удалено {file_name} из облака')

    def get_info(self):
        return self.ya_disk.listdir(self.backup_folder)
