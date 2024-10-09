from ultralytics import YOLO
import os
import cv2
import numpy as np
import torch
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
# Load a pretrained YOLOv8n modeld
# model = YOLO('/media/abark/2fce48c5-6aff-4b5d-8579-0b1d2b28aefa/projects/yolo/gradio_app/v9c6400d.pt')
model = YOLO('/media/abark/2fce48c5-6aff-4b5d-8579-0b1d2b28aefa/projects/Waste_Management_System/runs/detect/train4/weights/best.onnx')
images = '/media/abark/2fce48c5-6aff-4b5d-8579-0b1d2b28aefa/projects/Waste_Management_System/test_data/input'
cropped_boxes = '/media/abark/2fce48c5-6aff-4b5d-8579-0b1d2b28aefa/projects/Waste_Management_System/test_data/output'
if not os.path.exists(cropped_boxes):
    os.mkdir(cropped_boxes)
for img in os.listdir(images):
    if img.lower().endswith(('.png', '.jpg', '.jpeg')):
        results = model(f'{images}/{img}', imgsz=640, conf=0.0, device=device, save=True, show_boxes=True, show_conf=True, show_labels=True)
        for r in results:
            # get x1, y1, x2, y2
            boxes = r.boxes.xyxy.cpu().numpy().squeeze().astype(np.int32)
            boxes = boxes.tolist()
            labels = r.boxes.cls.cpu().numpy().squeeze().astype(np.int32)
            labels = labels.tolist()
            print(boxes)
            print(labels)
            if len(boxes) > 0:
                try:
                    for box, label in zip(boxes, labels):
                        x1, y1, x2, y2 = box
                        # Add padding of 50 pixels
                        x1 = max(0, x1 - 50)
                        y1 = max(0, y1 - 50)
                        x2 = min(cv2.imread(f'{images}/{img}').shape[1], x2 + 50)
                        y2 = min(cv2.imread(f'{images}/{img}').shape[0], y2 + 50)
                        cv2_image = cv2.imread(f'{images}/{img}')
                        cv2_image = cv2_image[y1:y2, x1:x2]
                        # Check if the cropped image is valid
                        if cv2_image.size == 0:
                            print(f"Warning: Empty crop for image {img} with box {box}. Skipping.")
                            continue
                        # create folder name with label
                        if not os.path.exists(f'{cropped_boxes}/{label}'):
                            os.mkdir(f'{cropped_boxes}/{label}')
                        # save image with an incremented name
                        cv2.imwrite(f'{cropped_boxes}/{label}/{img}_{x1}_{y1}_{x2}_{y2}.png', cv2_image)
                except TypeError:
                    x1, y1, x2, y2 = boxes
                    label = labels
                    # Add padding of 50 pixels
                    x1 = max(0, x1 - 50)
                    y1 = max(0, y1 - 50)
                    x2 = min(cv2.imread(f'{images}/{img}').shape[1], x2 + 50)
                    y2 = min(cv2.imread(f'{images}/{img}').shape[0], y2 + 50)
                    cv2_image = cv2.imread(f'{images}/{img}')
                    cv2_image = cv2_image[y1:y2, x1:x2]
                    # Check if the cropped image is valid
                    if cv2_image.size == 0:
                        print(f"Warning: Empty crop for image {img} with box {box}. Skipping.")
                        continue
                    # create folder name with label
                    if not os.path.exists(f'{cropped_boxes}/{label}'):
                        os.mkdir(f'{cropped_boxes}/{label}')
                    # save image with an incremented name
                    cv2.imwrite(f'{cropped_boxes}/{label}/{img}_{x1}_{y1}_{x2}_{y2}.png', cv2_image)

