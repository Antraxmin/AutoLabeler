import cv2
import torch
from PIL import Image
import numpy as np
import yaml
from ultralytics import YOLO 

def load_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image file not found: {image_path}")
    return image

def detect_objects(image_path):
    model = YOLO('models/best.pt')
    results = model(image_path)

    detected_objects = []
    
    for result in results:
        # result에서 필요한 정보를 추출
        for obj in result.boxes:
            detected_object = {
                "class": obj.cls,  # 객체 클래스
                "bbox": obj.xyxy  # 경계 상자 (xmin, ymin, xmax, ymax)
            }
            detected_objects.append(detected_object)
        
        result.show()
        result.save(filename='uploads/result.jpg')
    
    return detected_objects
   


def save_labels(image_path, detected_objects):
    labels_path = image_path.replace('.jpg', '.txt').replace('.jpeg', '.txt').replace('.png', '.txt').replace('.bmp', '.txt')

    with open(labels_path, 'w') as f:
        for obj in detected_objects:
            f.write(f"{obj['class']} {obj['bbox'][0]} {obj['bbox'][1]} {obj['bbox'][2]} {obj['bbox'][3]}\n")

