from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit,
    QLineEdit, QPushButton, QLabel, QTabWidget
)
from instructo_ai import chat_response


class InstructoApp(QWidget):
    def __init__(self, component_name=""):
        super().__init__()
        self.setWindowTitle(f"Configurare pentru {component_name.upper()}")
        self.setGeometry(400, 200, 1000, 550)
        self.component_name = component_name.lower()

        layout = QVBoxLayout()

        # Tabs pentru cod
        self.tabs = QTabWidget()
        self.vhdl_tab = QTextEdit()
        self.vhdl_tab.setPlaceholderText("✍️ Scrie aici codul VHDL pentru configurare fizică")

        self.asm_tab = QTextEdit()
        self.asm_tab.setPlaceholderText("✍️ Scrie aici codul Assembly pentru configurare logică")

        self.tabs.addTab(self.vhdl_tab, "🧱 Configurare Fizică (VHDL)")
        self.tabs.addTab(self.asm_tab, "⚙️ Configurare Logică (Assembly)")
        self.tabs.currentChanged.connect(self.switch_chat_tab)

        # Chat AI – istoric separat
        self.chat_histories = {
            "vhdl": QTextEdit(),
            "assembly": QTextEdit()
        }
        for chat in self.chat_histories.values():
            chat.setReadOnly(True)

        self.input = QLineEdit()
        self.input.setPlaceholderText("Întreabă AI-ul despre codul scris...")
        self.send_btn = QPushButton("Trimite")
        self.send_btn.clicked.connect(self.handle_chat)

        self.current_chat_key = "vhdl"  # implicit

        # Chat layout
        self.chat_label = QLabel(f"🤖 Asistent AI – {self.component_name.upper()}")
        self.chat_area = QVBoxLayout()
        self.chat_area.addWidget(self.chat_label)
        self.chat_area.addWidget(self.chat_histories[self.current_chat_key])
        self.chat_area.addWidget(self.input)
        self.chat_area.addWidget(self.send_btn)

        # Layout general
        content_layout = QHBoxLayout()
        content_layout.addWidget(self.tabs, 3)

        chat_container = QWidget()
        chat_container.setLayout(self.chat_area)
        content_layout.addWidget(chat_container, 2)

        layout.addLayout(content_layout)
        self.setLayout(layout)

    def switch_chat_tab(self, index):
        # Comută între vhdl și assembly la schimbare tab
        new_key = "vhdl" if index == 0 else "assembly"
        if new_key == self.current_chat_key:
            return

        # Înlocuiește widgetul de chat
        self.chat_area.itemAt(1).widget().setParent(None)
        self.chat_area.insertWidget(1, self.chat_histories[new_key])
        self.current_chat_key = new_key

    def handle_chat(self):
        msg = self.input.text().strip()
        if not msg:
            return

        current_tab = self.tabs.currentIndex()
        cod = self.vhdl_tab.toPlainText() if current_tab == 0 else self.asm_tab.toPlainText()
        limbaj = "vhdl" if current_tab == 0 else "assembly"

        prompt = f"""
Întrebare: {msg}
Componentă: {self.component_name.upper()}
Limbaj: {limbaj.upper()}

Cod curent:
{cod}

Răspunde clar în română, explicând pe înțelesul unui student.
"""

        response = chat_response(prompt)
        self.chat_histories[self.current_chat_key].append(f"Tu: {msg}")
        self.chat_histories[self.current_chat_key].append(f"Instructo: {response}\n")
        self.input.clear()
