import os
import requests
import json
from pymongo import MongoClient
import re

# MongoDB connection URI
client = MongoClient('mongodb+srv://junaid_abark_db:Junaid-ABARK@junaid-abark-cluster.frhvckd.mongodb.net/?retryWrites=true&w=majority&appName=Junaid-ABARK-Cluster')

# Access the 'wastedata' database and 'wastes' collection
db = client['wastedata']
collection = db['wastes']

# Directory to save images and annotations
save_dir = 'data/images'
annotations_dir = 'data/annotations'
os.makedirs(save_dir, exist_ok=True)
os.makedirs(annotations_dir, exist_ok=True)

# Function to detect if a label is in English
def is_english(text):
    return re.match(r'^[a-zA-Z0-9\s\.,!?\'"]+$', text) is not None

# Function to detect if a label is in French (assuming any non-ASCII character is French)
def is_french(text):
    return any(ord(char) > 127 for char in text)

# Function to decode Unicode-escaped characters in labels
def decode_label(label):
    try:
        # Decode Unicode-escaped characters
        return label.encode().decode('unicode_escape')
    except Exception as e:
        # If decoding fails, return the label as-is
        print(f"Failed to decode label: {label} - {str(e)}")
        return label

# Step 1: Count the number of documents in the 'wastes' collection
document_count = collection.count_documents({})
print(f"Number of documents in 'wastes' collection: {document_count}")

# Step 2: Iterate through each document to download images and save labels
for document in collection.find():
    image_path = document.get('image_path', None)
    annotations = document.get('annotations', {}).get('annotations', [])  # Fixing the extraction of annotations
    
    if not image_path:
        print(f"Skipping document due to missing image path: {document['_id']}")
        continue

    # Step 3: Construct the image URL (replace with the correct base URL if necessary)
    image_url = f"https://api.wastedata.py.abark.com.pk/{image_path}"
    
    # Remove "_out" if it exists in the image filename
    image_filename_clean = os.path.basename(image_path).replace("_out", "")
    image_filename = os.path.join(save_dir, image_filename_clean)

    # Step 4: Download the image
    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            with open(image_filename, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded: {image_filename}")

            # Step 5: Save all annotations related to the image
            annotation_data = []

            for annotation in annotations:
                if isinstance(annotation, dict):  # Ensure the annotation is a dictionary
                    label = annotation.get('label', '') or 'Unknown'  # Handle empty labels

                    # Decode the label to handle any Unicode-escaped characters
                    label = decode_label(label)

                    # Append all labels, no skipping
                    x1 = annotation.get('x1', 0)
                    y1 = annotation.get('y1', 0)
                    x2 = annotation.get('x2', 0)
                    y2 = annotation.get('y2', 0)

                    annotation_data.append({
                        "label": label,
                        "coordinates": {
                            "x1": x1,
                            "y1": y1,
                            "x2": x2,
                            "y2": y2
                        }
                    })

            # Step 6: Save the annotations as a JSON file, using the same base name as the image
            image_base_name = os.path.splitext(image_filename_clean)[0]  # Extract base name without extension
            annotation_filename = os.path.join(annotations_dir, image_base_name + ".json")  # Save JSON with same base name
            with open(annotation_filename, 'w', encoding='utf-8') as annotation_file:  # Ensure UTF-8 encoding to handle French
                json.dump(annotation_data, annotation_file, ensure_ascii=False, indent=4)
            print(f"Annotations saved: {annotation_filename}")

        else:
            print(f"Failed to download image from {image_url} (Status code: {response.status_code})")
    except Exception as e:
        print(f"Error downloading image {image_url}: {str(e)}")
        continue

print("All images and annotations processed.")
