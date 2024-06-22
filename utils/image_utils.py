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
        for obj in result.boxes:
            bbox_tensor = obj.xyxy
            bbox_list = bbox_tensor.tolist()

            if isinstance(bbox_list[0], list):
                bbox_list = bbox_list[0]

            detected_object = {
                "class": obj.cls.item(),  
                "bbox": bbox_list 
            }
            detected_objects.append(detected_object)
        
    return detected_objects
   
def save_labels(image_path, detected_objects):
    labels_path = image_path.replace('.jpg', '.txt').replace('.jpeg', '.txt').replace('.png', '.txt').replace('.bmp', '.txt')

    with open(labels_path, 'w') as f:
        for obj in detected_objects:
            f.write(f"{obj['class']} {obj['bbox'][0]} {obj['bbox'][1]} {obj['bbox'][2]} {obj['bbox'][3]}\n")

