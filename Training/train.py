import torch
from yolov11 import YOLOv11  # Assuming YOLOv11 is available
from yolov11.utils import datasets, train

# Set up the device for training (GPU if available)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load the model (YOLOv11l)
model = YOLOv11(model_size='l').to(device)

# Path to your YAML file
yaml_path = 'Training/dataset.yaml'

# Load the dataset
train_dataset = datasets.load_dataset(yaml_path, mode='train')
val_dataset = datasets.load_dataset(yaml_path, mode='val')

# Training parameters
epochs = 100
batch_size = 16
learning_rate = 0.001
weight_decay = 0.0005

# Train the model
train.train_model(
    model=model,
    train_data=train_dataset,
    val_data=val_dataset,
    epochs=epochs,
    batch_size=batch_size,
    lr=learning_rate,
    weight_decay=weight_decay,
    device=device
)

# Save the trained model
torch.save(model.state_dict(), 'Training/yolov11l_trained_model.pth')

print("Training completed and model saved.")
