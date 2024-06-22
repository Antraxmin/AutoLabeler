from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtWidgets import QGraphicsPolygonItem

class PolygonTool(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setRenderHint(QPainter.Antialiasing)

        self.pen = QPen(Qt.blue)
        self.pen.setWidth(2)
        self.polygon_item = None
        self.polygon_points = []

    def mousePressEvent(self, event):
        if not self.polygon_item:
            self.polygon_item = QGraphicsPolygonItem()
            self.polygon_item.setPen(self.pen)
            self.scene.addItem(self.polygon_item)

        point = self.mapToScene(event.pos())
        self.polygon_points.append(point)
        polygon = self.polygon_item.polygon()
        polygon.append(QPointF(point.x(), point.y()))
        self.polygon_item.setPolygon(polygon)

    def mouseDoubleClickEvent(self, event):
        if self.polygon_item:
            self.polygon_item = None
            self.polygon_points = []