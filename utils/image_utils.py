import cv2
import torch
from PIL import Image
import numpy as np
import yaml

def load_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image file not found: {image_path}")
    return image

def detect_objects(image):
    with open('config/config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    
    model = torch.hub.load('ultralytics/yolov5', config['model']['name'])
    results = model(image)

    detected_objects = []
    for *box, conf, cls in results.xyxy[0]:
        detected_objects.append({
            'class': model.names[int(cls)],
            'bbox': [int(x) for x in box],
            'confidence': float(conf)
        })
    
    return detected_objects

def save_labels(image_path, detected_objects):
    labels_path = image_path.replace('.jpg', '.txt').replace('.jpeg', '.txt').replace('.png', '.txt').replace('.bmp', '.txt')

    with open(labels_path, 'w') as f:
        for obj in detected_objects:
            f.write(f"{obj['class']} {obj['bbox'][0]} {obj['bbox'][1]} {obj['bbox'][2]} {obj['bbox'][3]}\n")

