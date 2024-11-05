import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin

def download_images_from_pages(urls, keywords=None, folder_name="images"):
    # Create a main folder to save images from all pages
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
    }

    # Iterate over each URL in the list
    for page_index, url in enumerate(urls, start=1):
        # Create a subfolder for each page to avoid overwriting images
        page_folder = os.path.join(folder_name, f"page_{page_index}")
        if not os.path.exists(page_folder):
            os.makedirs(page_folder)

        # Send a request to the website
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to access {url}")
            continue

        # Parse the website HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all image tags with different possible sources
        img_tags = soup.find_all('img')

        # Track image download count per page
        download_count = 0

        for img in img_tags:
            # Try fetching image URLs from different possible attributes
            img_url = img.get('src') or img.get('data-src') or img.get('data-lazy')
            img_alt = img.get('alt', '')

            # Skip if img_url is missing
            if img_url is None:
                continue

            # Convert to full URL if relative
            img_url = urljoin(url, img_url)

            # Ensure img_alt is a string for comparison
            img_alt = img_alt.lower() if img_alt else ''

            # Download images based on keywords or download all if keywords are not provided
            if not keywords or any(keyword.lower() in img_url.lower() or keyword.lower() in img_alt for keyword in keywords):
                try:
                    img_data = requests.get(img_url, headers=headers).content
                    img_name = os.path.join(page_folder, f"image_{download_count + 1}.jpg")
                    
                    with open(img_name, 'wb') as img_file:
                        img_file.write(img_data)

                    print(f"Downloaded {img_name} from {url}")
                    download_count += 1

                except Exception as e:
                    print(f"Failed to download {img_url} from {url}: {e}")

        if download_count == 0:
            print(f"No images found matching the criteria on {url}.")
        else:
            print(f"Downloaded {download_count} images from {url}.")

# Example usage
urls = [
    "https://www.istockphoto.com/search/more-like-this/1490701077?assettype=image",
    "" # Add more URLs here
]

# With keywords
keywords = ["metal wastes", "scrap metal"]
download_images_from_pages(urls, keywords)

# Without keywords (download all images)
download_images_from_pages(urls)
