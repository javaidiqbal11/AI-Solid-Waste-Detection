import os
import shutil

# Folder paths
images_folder = "C:/Users/Admin/Downloads/Data_Normalization/export1/images"
labels_folder = "C:/Users/Admin/Downloads/Data_Normalization/export1/labels"
output_images_folder = "C:/Users/Admin/Downloads/Data_Normalization/data/output_images"
output_labels_folder = "C:/Users/Admin/Downloads/Data_Normalization/data/output_labels"

# Create output directories if they don't exist
os.makedirs(output_images_folder, exist_ok=True)
os.makedirs(output_labels_folder, exist_ok=True)

# Label mapping: {Actual Label: (Convert Label, Class Name)}
label_map = {
    12: (0, "Glass wastes"),
    20: (1, "Paper and cardboard wastes"),
    21: (2, "Plastic wastes"),
    30: (3, "Textile wastes"),
    34: (4, "Vegetal wastes")
}

# Helper function to process each label file
def process_label_file(label_file_path):
    # Read the label file and filter for specified labels
    filtered_labels = []
    with open(label_file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            label_info = line.strip().split()
            if label_info:
                actual_label = int(label_info[0])

                # If the label is in our specified list, convert and keep it
                if actual_label in label_map:
                    convert_label = label_map[actual_label][0]
                    label_info[0] = str(convert_label)
                    filtered_labels.append(" ".join(label_info))

    return filtered_labels

# Iterate over all label files in the labels folder
for label_file in os.listdir(labels_folder):
    label_file_path = os.path.join(labels_folder, label_file)
    image_file_path = os.path.join(images_folder, label_file.replace('.txt', '.jpg'))

    # Check if the corresponding image file exists
    if not os.path.exists(image_file_path):
        continue

    # Process the label file to filter and convert labels
    filtered_labels = process_label_file(label_file_path)

    # If there are no valid labels, discard the label and image files
    if filtered_labels:
        # Save the processed labels to the output folder
        with open(os.path.join(output_labels_folder, label_file), 'w') as file:
            file.write("\n".join(filtered_labels))

        # Copy the corresponding image to the output folder
        shutil.copy(image_file_path, output_images_folder)
    else:
        # If no valid labels found, remove both image and label files from output
        image_output_path = os.path.join(output_images_folder, label_file.replace('.txt', '.jpg'))
        if os.path.exists(image_output_path):
            os.remove(image_output_path)

print("Processing complete. Check the output folders for results.")
