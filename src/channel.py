import json
import os

# необходимо установить через: pip install google-api-python-client
from googleapiclient.discovery import build

import isodate


class Channel:
    '''Класс для ютуб-канала'''

    def __init__(self, channel_id: str) -> None:
        '''
        Экземпляр инициализируется id канала.
        Дальше все данные будут подтягиваться по API.
        '''
        
        self.__channel_id = channel_id

        # API_KEY скопирован из гугла и вставлен в переменные окружения
        self.api_key: str = os.getenv('API_KEY')
        
        # создать специальный объект для работы с API
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)

        self.channel = self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.title = self.channel['items'][0]['snippet']['title']
        self.video_count = self.channel['items'][0]['statistics']['videoCount']
        self.url = 'https://www.youtube.com/channel/' + self.__channel_id
        self.subscriberCount = self.channel['items'][0]['statistics']['subscriberCount']
        self.viewCount = self.channel['items'][0]['statistics']['viewCount']

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.channel, indent=2, ensure_ascii=False))
    
    @classmethod
    def get_service(cls):
        '''
        Классовый метод, возвращает объект для работы с YouTube API
        Не привязанный к классу
        '''
    
        # API_KEY скопирован из гугла и вставлен в переменные окружения
        api_key: str = os.getenv('API_KEY')
    
        # создать специальный объект для работы с API
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube
    
    def to_json(self, name_file):
        '''
        Выводит в файл name_file полученные данные
        '''
        with open(name_file, 'w', encoding='utf-8') as f:
            f.write(json.dumps(self.channel, indent=2, ensure_ascii=False))
