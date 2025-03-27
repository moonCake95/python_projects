import sys
from PySide6.QtWidgets import QApplication
from ui_main import MainUi

# Entry point of the application
def main():
  app = QApplication(sys.argv) # Create the application
  window = MainUi()            # Create an instance of our main UI class
  window.show()                # Show the main window
  sys.exit(app.exec())         # Start the application event loop

if __name__ == '__main__':
  main()