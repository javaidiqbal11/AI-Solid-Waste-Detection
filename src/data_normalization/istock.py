import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, quote
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import mimetypes

def create_directory(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
        print(f"Created directory: {dir_name}")
    else:
        print(f"Directory already exists: {dir_name}")

def get_dynamic_page_content(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "img"))
        )
    except Exception as e:
        print(f"Error waiting for page to load: {e}")
    
    page_content = driver.page_source
    driver.quit()
    return page_content

def get_image_urls(page_content, base_url):
    soup = BeautifulSoup(page_content, 'html.parser')
    image_urls = []
    images = soup.find_all('img')
    print(f"Found {len(images)} <img> elements.")
    
    for img in images:
        src = img.get('src') or img.get('data-src')
        if src:
            url = urljoin(base_url, src)
            image_urls.append(url)
    
    print(f"Extracted {len(image_urls)} image URLs (including duplicates).")
    return image_urls

def get_extension_from_content_type(content_type):
    extension = mimetypes.guess_extension(content_type)
    if extension:
        return extension
    else:
        if content_type == 'image/svg+xml':
            return '.svg'
        elif content_type == 'image/webp':
            return '.webp'
        else:
            return '.jpg'

def download_image(image_url, folder_path, headers, base_name, count):
    try:
        response = requests.get(image_url, headers=headers, stream=True, timeout=15)
        response.raise_for_status()

        content_type = response.headers.get('Content-Type', '').split(';')[0]
        if content_type != 'image/jpeg':
            print(f"Skipped (not JPEG): {image_url} [Content-Type: {content_type}]")
            return False

        new_filename = f"{base_name}_{count}.jpg"
        file_path = os.path.join(folder_path, new_filename)

        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(1024):
                if chunk:
                    f.write(chunk)
        print(f"Downloaded: {new_filename}")
        return True

    except requests.exceptions.RequestException as e:
        print(f"Failed to download {image_url}: {e}")
        return False
    except Exception as e:
        print(f"An error occurred while downloading {image_url}: {e}")
        return False

def main():
    # Get user input for search terms
    search_term = input("Enter your search term: ")
    encoded_search_term = quote(search_term)  # URL-encode the search term

    base_url = "https://www.istockphoto.com/photo/truckload-of-scrap-metal-gm157437836-10407559"
    start_page = 1  # Starting page number
    end_page = 1    # Ending page number (inclusive)

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/114.0.0.0 Safari/537.36"
        )
    }

    folder_name = search_term.replace(' ', '_')  # Create folder based on search term
    create_directory(folder_name)
    base_name = folder_name
    count = 1

    for page in range(start_page, end_page + 1):
        page_url = f"{base_url}?page={page}&phrase={encoded_search_term}"
        print(f"Fetching images from: {page_url}")
        page_content = get_dynamic_page_content(page_url)
        image_urls = get_image_urls(page_content, page_url)

        for img_url in image_urls:
            success = download_image(img_url, folder_name, headers, base_name, count)
            if success:
                count += 1

    print("Image downloading completed.")

if __name__ == "__main__":
    main()
