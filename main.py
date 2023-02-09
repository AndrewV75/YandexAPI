import requests
from decouple import config

''' У Яндекс.Диска есть очень удобное и простое API. Для описания всех его методов существует 
Полигон. Нужно написать программу, которая принимает на вход путь до файла на компьютере и 
сохраняет на Яндекс.Диск с таким же именем. Все ответы приходят в формате json;
Загрузка файла по ссылке происходит с помощью метода put и передачи туда данных;
Токен можно получить кликнув на полигоне на кнопку "Получить OAuth-токен".'''

token = config('token', default='')

class YandexDisk:

    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def get_files_list(self):
        files_url = 'https://cloud-api.yandex.net/v1/disk/resources/files'
        headers = self.get_headers()
        response = requests.get(files_url, headers=headers)
        return response.json()

    def _get_upload_link(self, path_to_file):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        params = {"path": path_to_file, "overwrite": "true"}
        response = requests.get(upload_url, headers=headers, params=params)
        # pprint(response.json())
        return response.json()

    def upload_file_to_disk(self, path_to_file, file_name):
        result = self._get_upload_link(path_to_file=path_to_file)
        url = result.get('href')
        response = requests.put(url, data=open(file_name, 'rb'))
        response.raise_for_status()
        # if response.status_code == 201:
        #     print("Success")


if __name__ == '__main__':
    # Получить путь к загружаемому файлу и токен от пользователя
    path_to_file = '/text.txt'
    token = config('token', default='')
    file_name = 'text.txt'
    uploader = YandexDisk(token=token)
    result = uploader.upload_file_to_disk(path_to_file, file_name)