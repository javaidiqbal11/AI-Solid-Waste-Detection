import os

def count_unmatched_files(images_folder, labels_folder):
    # Get list of files in both folders without file extensions
    image_files = {os.path.splitext(f)[0] for f in os.listdir(images_folder) if os.path.isfile(os.path.join(images_folder, f))}
    label_files = {os.path.splitext(f)[0] for f in os.listdir(labels_folder) if os.path.isfile(os.path.join(labels_folder, f))}

    # Find unmatched files
    unmatched_images = image_files - label_files
    unmatched_labels = label_files - image_files

    # Count unmatched files
    total_unmatched = len(unmatched_images) + len(unmatched_labels)

    print("Unmatched image files:", len(unmatched_images))
    print("Unmatched image file names:", unmatched_images)
    print("Unmatched label files:", len(unmatched_labels))
    print("Unmatched label file names:", unmatched_labels)
    print("Total unmatched files:", total_unmatched)

    return unmatched_images, unmatched_labels, total_unmatched

# Replace 'images' and 'labels' with the paths to your folders
images_folder = 'C:/Users/Admin/Downloads/Data_Normalization/data/train/images'
labels_folder = 'C:/Users/Admin/Downloads/Data_Normalization/data/train/labels'
count_unmatched_files(images_folder, labels_folder)
