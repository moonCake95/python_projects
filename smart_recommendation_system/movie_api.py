import os
import requests
from dotenv import load_dotenv


# Load TMDB API key from .env file
load_dotenv()
TMDB_API_KEY = os.getenv('TMDB_API_KEY')

class MovieAPI:
  '''Handle interaction with the Movie Database (TMDB) API.'''
  
  BASE_URL = 'https://api.themoviedb.org/3'
  
  def __init__(self):
    if not TMDB_API_KEY:
      raise ValueError('TMDB API key is missing. Please set it in the .env file.')
    self.api_key = TMDB_API_KEY
  
  def search_movies(self, query):
    '''
    Search for movies using a query string.
    
    :param query: str - The movie name or keyword to search bar.
    :return: list of matching movies (dicts).
    '''
    
    url = f'{self.BASE_URL}/search/movie'
    params = {
      'api_key': self.api_key,
      'query': query,
      'language': 'en-US'
    }
    
    try:
      response = requests.get(url, params=params)
      response.raise_for_status()
      data = response.json()
      return data.get('results', [])
    except requests.RequestException as e:
      print(f'Error while searching movies: {e}')
      return []
          
  def get_poster_pixmap(self, poster_path):
    """
    Download a movie poster and return it as a QPixmap.

    :param poster_path: str - The relative path to the poster image.
    :return: QPixmap or None if failed.
    """
    from PySide6.QtGui import QPixmap
    if not poster_path:
      return None
    url = f"https://image.tmdb.org/t/p/w200{poster_path}"
    try:
      response = requests.get(url)
      response.raise_for_status()
      pixmap = QPixmap()
      pixmap.loadFromData(response.content)
      return pixmap
    except requests.RequestException as e:
      print(f"Error loading poster: {e}")
      return None