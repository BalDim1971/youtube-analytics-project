########################################################################################################
# Файл с описанием класса Playlist
########################################################################################################

import datetime
import os
# необходимо установить через: pip install google-api-python-client
from googleapiclient.discovery import build

import isodate


class PlayList:
    '''
    Описание класса
    Атрибуты:
    - название плейлиста
    - ссылку на плейлист
    Методы:
    - total_duration` возвращает объект класса `datetime.timedelta` с суммарной длительность плейлиста, работает @property
    - show_best_video(), возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)
    '''
    
    def __init__(self, id_playlist: str):
        '''
        Конструктор класса, параметр идентификатор плейлиста
        '''
        
        playlist = self.get_service().playlists().list(id=id_playlist, part='snippet').execute()
        self.title = playlist['items'][0]['snippet']['title']
        self.url = "https://www.youtube.com/playlist?list=" + id_playlist
        
        # Получить содержимое плейлиста
        content = self.get_service().playlistItems().list(playlistId=id_playlist, part='contentDetails').execute()
        
        # получить все id видеороликов из плейлиста
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in content['items']]
        
        # вывести длительности видеороликов из плейлиста
        self.__video_response = self.get_service().videos().list(part='contentDetails,statistics', id=','.join(video_ids)).execute()
        
    @classmethod
    def get_service(cls):
        '''
        Классовый метод, возвращает объект для работы с YouTube API
        Не привязанный к классу
        '''
        
        # API_KEY скопирован из гугла и вставлен в переменные окружения
        api_key: str = os.getenv('API_KEY')
        
        # создать специальный объект для работы с API
        return build('youtube', 'v3', developerKey=api_key)
    
    def show_best_video(self) -> str:
        '''
        Вернуть ссылку на лучшее видео по количеству лайков
        '''
       	
        # Инициируем временные переменные
        count_like_best_video = 0
        url_best_video = ''
        
        # Обходим видео
        for video in self.__video_response['items']:
            # получить статистику видео и лайки
            like_count = video['statistics']['likeCount']
            if int(like_count) > int(count_like_best_video):
                count_like_best_video = like_count
                url_best_video = "https://youtu.be/" + video['id']
        
        return url_best_video
        
    
    @property
    def total_duration(self) -> datetime.timedelta:
        my_time = datetime.timedelta(0)
        for video in self.__video_response['items']:
            duration = isodate.parse_duration(video['contentDetails']['duration'])
            my_time += duration
        return my_time
