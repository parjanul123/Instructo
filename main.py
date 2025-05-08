import sys
from PyQt6.QtWidgets import QApplication
from instructo_gui import StartWindow  # Asigură-te că numele fișierului e exact 'Instructo_gui.py'

def run_gui():
    app = QApplication(sys.argv)
    start_window = StartWindow()
    start_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    run_gui()
