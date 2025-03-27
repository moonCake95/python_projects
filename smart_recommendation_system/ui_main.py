from PySide6.QtGui import QFont, QIcon, QStandardItemModel, QStandardItem, QPixmap, QPainter, QColor
from PySide6.QtCore import Qt, QSize
from movie_api import MovieAPI
from PySide6.QtWidgets import (
                        QWidget, 
                        QVBoxLayout, 
                        QLabel, 
                        QLineEdit, 
                        QPushButton,
                        QListView,
                        QHBoxLayout
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
    self.layout.setContentsMargins(0, 0, 0, 0)

    self.title_label = QLabel('Smart Recommendation System')
    self.title_label.setAlignment(Qt.AlignCenter)
    self.title_label.setFont(QFont('Arial', 25, QFont.Bold))
    self.title_label.setStyleSheet("color: #FFD700; margin-bottom: 0px;")
    
    self.search_input = QLineEdit()
    self.search_input.setPlaceholderText('Enter a movie name...')
    self.search_input.setFont(QFont('Arial', 14))
    self.search_input.setStyleSheet('padding: 6px; border-radius: 6px; border: 1px solid #555;')
    
    self.search_button = QPushButton('Search')
    self.search_button.setFont(QFont("Arial", 14, QFont.Bold))
    self.search_button.clicked.connect(self.handle_search)
    self.search_button.setStyleSheet('''
        QPushButton {
          background-color: #444;
          color: white;
          border: none;
          padding: 6px 12px;
          border-radius: 6px;
        }
        QPushButton:hover {
          background-color: #666
        }
    ''')
    
    self.results_list = QListView()
    self.results_list.setViewMode(QListView.IconMode)
    self.results_list.setIconSize(QSize(150, 250))
    self.results_list.setResizeMode(QListView.Adjust)
    self.results_list.setSpacing(5)
    self.results_list.setContentsMargins(0, 0, 0, 0)
    self.results_list.setStyleSheet("""
        QListView::viewport {
            margin: 0px;
            padding: 0px;
        }
        QListView {
            spacing: 0px;
            padding: 0px;
            margin: 0px;
            border: none;
        }
    """)
    self.model = QStandardItemModel()
    self.results_list.setModel(self.model)
    
    #  Add widgets to layout
    self.layout.addWidget(self.title_label)
    
    search_layout = QHBoxLayout()
    search_layout.setContentsMargins(20, 0, 20, 0)  # Adds margin left/right
    search_layout.addWidget(self.search_input, stretch=3)
    search_layout.addWidget(self.search_button, stretch=1)
    self.layout.addLayout(search_layout)
    
    self.layout.addWidget(self.results_list)
    
    self.setLayout(self.layout)

  def handle_search(self):
    '''
    Triggered when the search button is clicked.
    Calls the MovieAPI to search for movies and display them.
    '''
    
    query = self.search_input.text()
    self.model.clear()
    
    if not query:
      item = QStandardItem('Please enter a movie name.')
      item.setEditable(False)
      self.model.appendRow(item)
      return
    
    results = self.movie_api.search_movies(query)
    
    if results:
      for movie in results:
        poster_path = movie.get('poster_path')
        title = movie.get('title', 'Unknown Title')

        pixmap = self.movie_api.get_poster_pixmap(poster_path)

        if pixmap:
          icon = QIcon(pixmap)
          item = QStandardItem()
          item.setIcon(icon)
          item.setText("")  # כדי להסתיר כיתוב
          item.setEditable(False)
        else:
          # Create a black placeholder pixmap
          placeholder_pixmap = QPixmap(150, 225)
          placeholder_pixmap.fill(QColor('black'))

          painter = QPainter(placeholder_pixmap)
          painter.setPen(QColor('white'))
          painter.setFont(QFont('Arial', 12, QFont.Bold))
          painter.drawText(placeholder_pixmap.rect(), Qt.AlignCenter, title)
          painter.end()

          icon = QIcon(placeholder_pixmap)
          item = QStandardItem()
          item.setIcon(icon)
          item.setText("")  # No label below the icon
          item.setEditable(False)

        self.model.appendRow(item)

    else:
      item = QStandardItem('No results found.')
      item.setEditable(False)
      self.model.appendRow(item)