from PyQt6.QtWidgets import QGraphicsView
from PyQt6.QtGui import QPainter
from PyQt6.QtCore import QMimeData, Qt

class CanvasView(QGraphicsView):
    def __init__(self, scene, parent=None):
        super().__init__(scene)
        self.parent = parent  # referință la SimulationWindow
        self.setAcceptDrops(True)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        component_name = event.mimeData().text()
        pos = self.mapToScene(event.position().toPoint())
        self.parent.add_component_at(component_name, pos)
        event.acceptProposedAction()
