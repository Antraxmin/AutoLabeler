from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen

class BoundingBoxTool(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setRenderHint(QPainter.Antialiasing)

        self.pen = QPen(Qt.red)
        self.pen.setWidth(2)
        self.current_rect = None
        self.start_point = None