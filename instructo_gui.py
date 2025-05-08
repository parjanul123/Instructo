# Instructo_gui.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel
)
from PyQt6.QtCore import Qt
from SimulationWindow import SimulationWindow


class StartWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Instructo - Start")
        self.setGeometry(400, 200, 400, 200)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        title = QLabel("🧠 Instructo IDE")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold;")

        new_button = QPushButton("📁 New Project")
        new_button.clicked.connect(self.launch_new_project)

        layout.addStretch()
        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(new_button)
        layout.addStretch()
        self.setLayout(layout)

    def launch_new_project(self):
        self.sim_window = SimulationWindow()
        self.sim_window.show()
        self.close()
