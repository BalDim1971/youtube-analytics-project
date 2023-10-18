#################################################################################################
# Описание одного потока видео
#################################################################################################

import os

# необходимо установить через: pip install google-api-python-client
from googleapiclient.discovery import build


class Video:
	'''
	Класс с данными о видео файле на Youtube:
	- id видео
	- название видео
	- ссылка на видео
	- количество просмотров
	- количество лайков
	'''
	
	def __init__(self, id_video: str):
		'''
		Экземпляр инициализируется id video.
		Дальше все данные будут подтягиваться по API.
		'''
		
		self.id_video = id_video
		self.content = self.get_service().videos().list(id=self.id_video, part='snippet, statistics').execute()
		
		try:
			self.title = self.content['items'][0]['snippet']['title']

			self.url_video = 'https://youtu.be/' + self.id_video
			self.count_of_view = self.content['items'][0]['statistics']['viewCount']
			self.like_count = self.content['items'][0]['statistics']['likeCount']
		
		except IndexError:
			self.title = None
			self.url_video = None
			self.count_of_view = None
			self.like_count = None
	
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
	
	def __str__(self) -> str:
		'''
		Магический метод, возвращающий название видео
		'''
		return f'{self.title}'


class PLVideo(Video):
	'''
	Класс для видео в плейлисте. Наследник Video
	Добавлен параметр:
	- id плейлиста
	'''
	
	def __init__(self, id_video: str, id_playlist: str):
		'''
		Инициализируем по id_video и id_playlist
		Параметр id_video передаем в базовый класс
		'''
		
		super().__init__(id_video)
		self.id_playlist = id_playlist
