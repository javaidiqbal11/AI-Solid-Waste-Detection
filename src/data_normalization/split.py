import os
import shutil
import random

# Define paths (update these according to your actual dataset structure)
dataset_dir = 'C:/Users/Admin/Downloads/Data_Normalization/data'
image_dir = os.path.join(dataset_dir, 'images')
label_dir = os.path.join(dataset_dir, 'labels')

# Create directories for train and test sets with images and labels subfolders
train_img_dir = os.path.join(dataset_dir, 'train', 'images')
test_img_dir = os.path.join(dataset_dir, 'test', 'images')
train_lbl_dir = os.path.join(dataset_dir, 'train', 'labels')
test_lbl_dir = os.path.join(dataset_dir, 'test', 'labels')

os.makedirs(train_img_dir, exist_ok=True)
os.makedirs(test_img_dir, exist_ok=True)
os.makedirs(train_lbl_dir, exist_ok=True)
os.makedirs(test_lbl_dir, exist_ok=True)

# Get all image filenames and corresponding labels (Update file extensions if using .png or other types)
image_files = [f for f in os.listdir(image_dir) if f.endswith('.jpg') and os.path.isfile(os.path.join(image_dir, f))]
label_files = [f.replace('.jpg', '.txt') for f in image_files]  # Assuming labels are in .txt format

# Pair images with labels
data = [(img, lbl) for img, lbl in zip(image_files, label_files) if os.path.exists(os.path.join(label_dir, lbl))]

# Shuffle the dataset for random splitting
random.seed(42)  # For reproducibility
random.shuffle(data)

# Split dataset into training and testing sets (80% training, 20% testing)
split_ratio = 0.8
split_index = int(len(data) * split_ratio)

train_data = data[:split_index]
test_data = data[split_index:]

# Function to move files
def move_files(data, src_img_dir, src_lbl_dir, dest_img_dir, dest_lbl_dir):
    for image_file, label_file in data:
        # Move images
        shutil.move(os.path.join(src_img_dir, image_file), os.path.join(dest_img_dir, image_file))
        # Move labels
        shutil.move(os.path.join(src_lbl_dir, label_file), os.path.join(dest_lbl_dir, label_file))

# Move files to 'train' and 'test' directories with images and labels subfolders
move_files(train_data, image_dir, label_dir, train_img_dir, train_lbl_dir)
move_files(test_data, image_dir, label_dir, test_img_dir, test_lbl_dir)

print("Dataset has been split and moved to 'train/images', 'train/labels', 'test/images', and 'test/labels' directories.")
