from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QTextEdit, QGraphicsScene,
    QLineEdit, QPushButton, QMenu, QGraphicsRectItem, QGraphicsSimpleTextItem, QInputDialog, QSplitter
)
from PyQt6.QtGui import QBrush, QColor, QPainter, QFont, QDrag
from PyQt6.QtCore import Qt, QMimeData
from ComponentConfig import InstructoApp
from Canvas_Views import CanvasView
from instructo_ai import chat_response  # ✅ Importăm funcția AI

# === Componenta grafică pentru fiecare obiect (CPU, RAM, etc.) ===
class ComponentItem(QGraphicsRectItem):
    def __init__(self, name, label):
        super().__init__(0, 0, 120, 60)
        self.name = name
        self.label = label
        self.setBrush(QBrush(QColor("lightblue")))
        self.setToolTip(f"{label}")
        self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsSelectable)

        self.text = QGraphicsSimpleTextItem(label, self)
        self.text.setBrush(QBrush(QColor("white")))
        self.text.setFont(QFont("Arial", 10))
        self.text.setPos(10, 65)

    def contextMenuEvent(self, event):
        menu = QMenu()
        config = menu.addAction("🛠 Configurează")
        rename = menu.addAction("✏️ Redenumește")
        copy = menu.addAction("📄 Copiază")
        delete = menu.addAction("🔚 Șterge")

        action = menu.exec(event.screenPos())

        if action == delete:
            self.scene().removeItem(self)
        elif action == copy:
            clone = ComponentItem(self.name, self.name)
            clone.setPos(self.pos().x() + 20, self.pos().y() + 20)
            self.scene().addItem(clone)
        elif action == config:
            self.config_window = InstructoApp(component_name=self.name)
            self.config_window.show()
        elif action == rename:
            new_name, ok = QInputDialog.getText(None, "Redenumește Componenta", "Introdu un nou nume:", text=self.name)
            if ok and new_name.strip():
                self.name = new_name.strip()
                self.text.setText(self.name)


# === Fereastra principală de simulare ===
class SimulationWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Instructo Wiring Simulator")
        self.setGeometry(200, 100, 1200, 700)

        central_widget = QWidget()
        central_layout = QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)

        self.scene = QGraphicsScene()
        self.view = CanvasView(self.scene, self)

        self.chat_wiring = QTextEdit()
        self.chat_wiring.setReadOnly(True)
        self.chat_input = QLineEdit()
        self.chat_button = QPushButton("Trimite")
        self.chat_button.clicked.connect(self.handle_chat)

        self.palette = QListWidget()
        self.palette.addItems(["CPU", "ALU", "GPU", "RAM", "ROM", "Register"])
        self.palette.setMaximumHeight(100)
        self.palette.setDragEnabled(True)
        self.palette.clicked.connect(self.add_component)
        self.palette.mouseMoveEvent = lambda event: self.start_drag()

        self.component_count = {}

        left_layout = QVBoxLayout()
        left_layout.addWidget(self.view)
        left_layout.addWidget(self.palette)
        left_container = QWidget()
        left_container.setLayout(left_layout)

        chat_layout = QVBoxLayout()
        chat_layout.addWidget(self.chat_wiring)
        chat_layout.addWidget(self.chat_input)
        chat_layout.addWidget(self.chat_button)
        right_container = QWidget()
        right_container.setLayout(chat_layout)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(left_container)
        splitter.addWidget(right_container)
        splitter.setSizes([900, 300])

        central_layout.addWidget(splitter)

    # === Adaugă componente pe scenă ===
    def add_component(self):
        selected_item = self.palette.currentItem().text()
        if selected_item:
            self.add_component_at(selected_item, None)

    def add_component_at(self, name, pos):
        base_name = name.lower()
        count = self.component_count.get(base_name, 0)
        label = f"{base_name}" if count == 0 else f"{base_name}{count}"
        self.component_count[base_name] = count + 1

        item = ComponentItem(name, label)
        if pos:
            item.setPos(pos)
        else:
            item.setPos(100, 100)
        self.scene.addItem(item)

    # === Drag & Drop pentru componente ===
    def start_drag(self):
        selected_item = self.palette.currentItem()
        if selected_item:
            mime = QMimeData()
            mime.setText(selected_item.text())
            drag = QDrag(self.palette)
            drag.setMimeData(mime)
            drag.exec()

    # === Funcție pentru chat AI ===
    def handle_chat(self):
        msg = self.chat_input.text().strip()
        if not msg:
            return

        self.chat_wiring.append(f"<b>Tu:</b> {msg}")

        # ✅ Trimitem întrebarea la OpenAI
        prompt = f"""
Tu ești un asistent tehnic pentru simulare și conectare componente (CPU, RAM, ALU, etc).
Răspunde clar și concis, ca pentru un student.

Întrebare:
{msg}

Explică cum să conectez componentele sau să le configurez în mod corect.
"""

        response = chat_response(prompt)  # ✅ Folosim OpenAI
        self.chat_wiring.append(f"<b>Instructo:</b> {response}\n")
        self.chat_input.clear()
