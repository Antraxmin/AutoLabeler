from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QFileDialog, QHBoxLayout, QMessageBox
from PyQt5.QtCore import Qt
import sys
import cv2
from utils.image_utils import detect_objects, load_image, save_labels

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AutoLabeler")
        self.setGeometry(100, 100, 1280, 720)

        self.main_layout = QVBoxLayout()
        
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.image_label)

        self.button_layout = QHBoxLayout()
        
        self.load_button = QPushButton("Load Image", self)
        self.load_button.clicked.connect(self.load_image)
        self.button_layout.addWidget(self.load_button)

        self.detect_button = QPushButton("Detect Objects", self)
        self.detect_button.clicked.connect(self.detect_image)
        self.button_layout.addWidget(self.detect_button)

        self.save_button = QPushButton("Save Labels", self)
        self.save_button.clicked.connect(self.save_labels)
        self.button_layout.addWidget(self.save_button)

        self.main_layout.addLayout(self.button_layout)
        
        self.main_widget = QWidget()
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)
        
        self.image_path = None
        self.image = None
        self.detected_objects = []

    def load_image(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Load Image", "", "Image Files (*.jpg *.jpeg *.png *.bmp)", options=options)
        if file_name:
            self.image_path = file_name
            self.image = load_image(self.image_path)
            self.display_image(self.image)

    def display_image(self, image):
        height, width, channel = image.shape
        bytes_per_line = 3 * width
        qimage = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)
        self.image_label.setPixmap(pixmap)

    def detect_image(self):
        if self.image is not None:
            detected_objects = detect_objects(self.image) 
            if detected_objects is not None:
                self.detected_objects = detected_objects
                self.display_detected_objects()
        else:
            QMessageBox.warning(self, "Warning", "Load an image first.")

    def display_detected_objects(self):
        if self.image is not None:
            image_with_boxes = self.image.copy()
            for obj in self.detected_objects:
                bbox = obj["bbox"]
                xmin, ymin, xmax, ymax = [int(coord) for coord in bbox]
                
                cv2.rectangle(image_with_boxes, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
        
        self.display_image(image_with_boxes)

    def save_labels(self):
        if self.detected_objects:
            save_labels(self.image_path, self.detected_objects)
            QMessageBox.information(self, "Info", "Labels saved successfully.")
        else:
            QMessageBox.warning(self, "Warning", "No objects detected to save.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
