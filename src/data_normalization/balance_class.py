import os
from collections import Counter

# Define directories
source_labels_dir = r"C:/Users/Admin/Downloads/Data_Normalization/data/labels"
source_images_dir = r"C:/Users/Admin/Downloads/Data_Normalization/data/images"

# Overall counter for all labels across all files
total_label_counts = Counter()
# List to hold files that contain only class '2'
class_2_only_files = []
# Iterate over each label file in the source labels directory
for label_filename in os.listdir(source_labels_dir):
    if label_filename.endswith('.txt'):
        label_path = os.path.join(source_labels_dir, label_filename)
        # Read all lines in the label file
        with open(label_path, 'r') as file:
            lines = file.readlines()
        # Get unique labels in the file
        labels_in_file = {line.split()[0] for line in lines}
        # Check if the file contains only class '2'
        if labels_in_file == {'2'}:
            class_2_only_files.append(label_filename)
        else:
            # Count labels if the file contains classes other than '2'
            label_count = Counter(line.split()[0] for line in lines)
            total_label_counts.update(label_count)
# Delete all files that contain only class '2' and their corresponding images
for label_filename in class_2_only_files:
    label_path = os.path.join(source_labels_dir, label_filename)
    image_filename = os.path.splitext(label_filename)[0] + '.jpg'
    image_path = os.path.join(source_images_dir, image_filename)

    # Delete the label file
    # os.remove(label_path)

    # print(f"Deleted label file: {label_filename}")
    # Delete the corresponding image file if it exists
    if os.path.exists(image_path):

        # os.remove(image_path)

        # print(f"Deleted corresponding image file: {image_filename}")
        pass
        # print(image_filename)

    else:
        # print(label_filename)
        pass

# Print the updated total count of each label across remaining files
print("Updated total counts for each label across remaining files:")
for label, count in total_label_counts.items():
    print(f"Label {label}: {count}")
