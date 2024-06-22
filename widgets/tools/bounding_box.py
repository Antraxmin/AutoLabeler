from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtWidgets import QGraphicsRectItem

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

    def mousePressEvent(self, event):
        self.start_point = event.pos()
        self.current_rect = QGraphicsRectItem()
        self.current_rect.setPen(self.pen)
        self.scene.addItem(self.current_rect)

    def mouseMoveEvent(self, event):
        if self.start_point:
            end_point = event.pos()
            rect = QRectF(self.start_point, end_point).normalized()
            self.current_rect.setRect(rect)

    def mouseReleaseEvent(self, event):
        self.start_point = None
        self.current_rect = None