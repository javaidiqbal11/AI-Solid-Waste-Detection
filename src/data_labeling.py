import json
import os
from PIL import Image  # Import the Pillow library for image processing

# Predefined 39 unique class labels (including "Unknown")
unique_class_labels = [
    "Spent solvents", "Acid, alkaline or saline wastes", "Used oils", "Spent chemical catalysts",
    "Chemical preparation wastes", "Chemical deposits and residues", "Industrial effluent sludges",
    "Sludges and liquid wastes from waste treatment", "Health care and biological wastes",
    "Metal waste, ferrous", "Metal waste, non-ferrous", "Metal wastes, mixed ferrous and non-ferrous",
    "Glass wastes", "Paper and cardboard wastes", "Rubber wastes", "Plastic wastes", "Wood wastes",
    "Textile wastes", "Waste containing PCB", "Discarded equipment", "Discarded vehicles",
    "Batteries and accumulators wastes", "Animal and mixed food waste", "Vegetal wastes",
    "Slurry and manure", "Household and similar wastes", "Mixed and undifferentiated materials",
    "Sorting residues", "Common sludges", "Construction and demolition wastes", "Asbestos waste",
    "Waste of naturally occurring minerals", "Combustion wastes", "Various mineral wastes", "Soils",
    "Dredging spoil", "Waste from waste treatment", "Solidified, stabilised or vitrified waste",
    "Unknown"  # Adding the "Unknown" class label as the 39th label
]

# Extended label mapping with French-to-English translations
label_mapping = {
    "Solvants usés": "Spent solvents",
    "Déchets acides, alcalins ou salins": "Acid, alkaline or saline wastes",
    "Huiles usagées": "Used oils",
    "Catalyseurs chimiques usés": "Spent chemical catalysts",
    "Déchets de préparations chimiques": "Chemical preparation wastes",
    "Dépôts et résidus chimiques": "Chemical deposits and residues",
    "Boues d'effluents industriels": "Industrial effluent sludges",
    "Boues et déchets liquides du traitement des déchets": "Sludges and liquid wastes from waste treatment",
    "Déchets de soins de santé et biologiques": "Health care and biological wastes",
    "Déchets métalliques, ferreux": "Metal waste, ferrous",
    "Déchets métalliques, non ferreux": "Metal waste, non-ferrous",
    "Déchets métalliques, mixtes ferreux et non ferreux": "Metal wastes, mixed ferrous and non-ferrous",
    "Déchets de verre": "Glass wastes",
    "Déchets de papier et de carton": "Paper and cardboard wastes",
    "Déchets de caoutchouc": "Rubber wastes",
    "Déchets plastiques": "Plastic wastes",
    "Déchets de bois": "Wood wastes",
    "Déchets textiles": "Textile wastes",
    "Déchets contenant des PCB": "Waste containing PCB",
    "Équipements mis au rebut": "Discarded equipment",
    "Véhicules mis au rebut": "Discarded vehicles",
    "Déchets de piles et accumulateurs": "Batteries and accumulators wastes",
    "Déchets alimentaires et mélangés d'origine animale": "Animal and mixed food waste",
    "Déchets végétaux": "Vegetal wastes",
    "Lisiers et fumiers": "Slurry and manure",
    "Déchets ménagers et assimilés": "Household and similar wastes",
    "Matériaux mélangés et non différenciés": "Mixed and undifferentiated materials",
    "Résidus de tri": "Sorting residues",
    "Boues communes": "Common sludges",
    "Déchets de construction et de démolition": "Construction and demolition wastes",
    "Déchets d'amiante": "Asbestos waste",
    "Déchets de minéraux naturels": "Waste of naturally occurring minerals",
    "Déchets de combustion": "Combustion wastes",
    "Divers déchets minéraux": "Various mineral wastes",
    "Sols": "Soils",
    "Dragages": "Dredging spoil",
    "Déchets provenant du traitement des déchets": "Waste from waste treatment",
    "Déchets solidifiés, stabilisés ou vitrifiés": "Solidified, stabilised or vitrified waste"
}

# Predefined dictionary to store the unique class number for each class label, including "Unknown"
class_to_index = {label: index for index, label in enumerate(unique_class_labels)}

# Convert label to English (if needed)
def convert_label_to_english(label):
    # Check if the label is in French and map it to English
    return label_mapping.get(label, label)

# Get the class index from predefined class_to_index (39 unique classes, including "Unknown")
def get_class_index(label):
    english_label = convert_label_to_english(label)  # Convert label to English
    # If the label is not in the predefined list, assign it to "Unknown"
    return class_to_index.get(english_label, class_to_index["Unknown"])

# Convert bounding box to YOLO format
def convert_bbox_to_yolo_format(bbox, img_width, img_height):
    x1, y1, x2, y2 = bbox['x1'], bbox['y1'], bbox['x2'], bbox['y2']
    
    # Compute the center of the bounding box
    x_center = (x1 + x2) / 2.0
    y_center = (y1 + y2) / 2.0
    
    # Compute the width and height of the bounding box
    width = x2 - x1
    height = y2 - y1
    
    # Normalize the values
    x_center /= img_width
    y_center /= img_height
    width /= img_width
    height /= img_height
    
    return x_center, y_center, width, height

# Get the dimensions of the image dynamically using Pillow (PIL)
def get_image_dimensions(image_filepath):
    with Image.open(image_filepath) as img:
        return img.size  # Returns (width, height)

# Process each JSON file to check contents and convert to YOLO format if applicable
def process_json_file(json_filepath, images_dir, output_dir):
    # Get the base filename without the extension
    base_name = os.path.splitext(os.path.basename(json_filepath))[0]

    # Construct the corresponding image path (assumed to be .jpg, but can adjust)
    image_filepath = os.path.join(images_dir, base_name + '.jpg')
    
    if not os.path.exists(image_filepath):
        print(f"Image file {image_filepath} not found for {json_filepath}")
        return
    
    # Get the actual image dimensions
    img_width, img_height = get_image_dimensions(image_filepath)
    
    # Prepare the label file corresponding to the image (save in output_dir with same base name)
    label_file = os.path.join(output_dir, base_name + '.txt')

    with open(json_filepath, 'r') as f:
        try:
            json_data = json.load(f)
        except json.JSONDecodeError:
            print(f"Invalid JSON in file: {json_filepath}")
            with open(label_file, 'w'):  # Create empty label file
                pass
            return

    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    valid_labels_found = False  # Track if we found any valid labels

    with open(label_file, 'w') as f:
        if not json_data:
            print(f"Empty JSON file: {json_filepath}")
            # Create an empty label file if the JSON is empty
            pass
        else:
            for obj in json_data:
                label = obj['label']
                bbox = obj['coordinates']
                
                # Convert label to class index (use predefined 39 unique classes, including "Unknown")
                class_idx = get_class_index(label)
                
                # Convert bounding box to YOLO format
                x_center, y_center, width, height = convert_bbox_to_yolo_format(bbox, img_width, img_height)
                
                # Write the YOLO formatted label data to the file
                f.write(f"{class_idx} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")
                valid_labels_found = True

    # Keep the .txt file, even if no valid labels are found (ensure equal number of files)
    if not valid_labels_found:
        with open(label_file, 'w'):  # Just create an empty .txt file
            pass
        print(f"No valid labels found in {json_filepath}, created empty {label_file}")

# Function to save the unique class-to-index mapping to a text file
def save_class_labels(output_dir):
    class_labels_file = os.path.join(output_dir, 'C:/Users/Admin/Downloads/Waste_Management/data/class_labels.txt')
    
    # Overwrite the file (not append) to ensure no repeated entries
    with open(class_labels_file, 'w') as f:
        for class_label, class_index in sorted(class_to_index.items(), key=lambda x: x[1]):
            f.write(f"{class_label}: {class_index}\n")
    
    print(f"Class labels saved to {class_labels_file}")

# Main function to iterate through the JSON files
def process_all_json_files(input_dir, images_dir, output_dir):
    for json_file in os.listdir(input_dir):
        if json_file.endswith('.json'):
            json_filepath = os.path.join(input_dir, json_file)
            print(f"Processing file: {json_file}")
            process_json_file(json_filepath, images_dir, output_dir)
    
    # Once all files are processed, save the final class-to-index mapping to a text file
    save_class_labels(output_dir)

# Sample usage
if __name__ == "__main__":
    # Directory containing the input JSON files
    input_dir = 'C:/Users/Admin/Downloads/Waste_Management/data/annotations'  # Change this to the actual directory containing JSON files
    
    # Directory containing the corresponding images
    images_dir = 'C:/Users/Admin/Downloads/Waste_Management/data/images'  # Change this to the actual directory containing images

    # Specific directory where the output YOLO .txt files and class labels will be saved
    output_dir = 'C:/Users/Admin/Downloads/Waste_Management/data/YOLO_Data'  # Change this to the desired output directory
    
    # Process all JSON files and save YOLO format files to the specified output directory
    process_all_json_files(input_dir, images_dir, output_dir)
