from ultralytics import YOLO

# Load a model
# model = YOLO("yolo11n.pt")  # load an official model
model = YOLO("/media/abark/2fce48c5-6aff-4b5d-8579-0b1d2b28aefa/projects/Waste_Management_System/runs/detect/train4/weights/best.pt")  # load a custom trained model

# Export the model
model.export(format="coreml")  #coreml #tflite