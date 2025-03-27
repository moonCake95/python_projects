from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from movie_api import MovieAPI
from PySide6.QtWidgets import (
                        QWidget, 
                        QVBoxLayout, 
                        QLabel, 
                        QLineEdit, 
                        QPushButton,
                        QListWidget,
                        QListWidgetItem
)

# ///////////////////////////// IMPORT TOOLS ↑ \\\\\\\\\\\\\\\\\\\\\\\\\\\\\

# ///////////////////////////// MAIN UI CLASS ↓ \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
class MainUi(QWidget):
  '''
  The main window UI for the Smart Recommendation System.
  '''
  
  def __init__(self):
    super().__init__()
    self.setWindowTitle('Smart Recommendation System')
    self.setMinimumSize(1000, 700)
    
    self.movie_api = MovieAPI() # Instantiate the API
    
    # UI Elements
    self.layout = QVBoxLayout()
    
    self.title_label = QLabel('Smart Recommendation System')
    self.title_label.setAlignment(Qt.AlignCenter)
    self.title_label.setFont(QFont('Arial', 25, QFont.Bold))
    self.title_label.setStyleSheet("color: #FFD700; margin-bottom: 10px;")
    
    self.search_input = QLineEdit()
    self.search_input.setPlaceholderText('Enter a movie name...')
    self.search_input.setFont(QFont('Arial', 14))
    self.search_input.setStyleSheet('padding: 10px; border-radius: 8px; border: 1px solid #555;')
    
    self.search_button = QPushButton('Search')
    self.search_button.setFont(QFont("Arial", 14, QFont.Bold))
    self.search_button.clicked.connect(self.handle_search)
    self.search_button.setStyleSheet('''
        QPushButton {
          background-color: #444;
          color: white;
          border: none;
          padding: 10px;
          margin-top: 10px;
          border-radius: 5px;
        }
        QPushButton:hover {
          background-color: #666
        }
    ''')
    
    self.results_list = QListWidget() # Will display movie title for now
    self.results_list.setFont(QFont('Arial', 13))
    self.results_list.setStyleSheet('padding: 5px;')
    
    #  Add widgets to layout
    self.layout.addWidget(self.title_label)
    self.layout.addWidget(self.search_input)
    self.layout.addWidget(self.search_button)
    self.layout.addWidget(self.results_list)
    
    self.setLayout(self.layout)

  def handle_search(self):
    '''
    Triggered when the search button is clicked.
    Calls the MovieAPI to search for movies and display them.
    '''
    
    query = self.search_input.text()
    self.results_list.clear()
    
    if not query:
      self.results_list.addItem('Please enter a movie name.')
      return
    
    results = self.movie_api.search_movies(query)
    
    if results:
      for movie in results:
        title = movie.get('title', 'Unknown Title')
        item = QListWidgetItem(title)
        self.results_list.addItem(item)
    else:
      self.results_list.addItem('No results found.')