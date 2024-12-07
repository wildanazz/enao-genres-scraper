import os
import time
import psycopg2
import pandas as pd
import re
from dotenv import load_dotenv
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

load_dotenv()

# Set up selenium driver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode
chrome_options.add_argument("--no-sandbox")  # Disables sandbox for Docker compatibility
chrome_options.add_argument("--disable-dev-shm-usage")  # Fixes some Chrome errors in Docker
chrome_options.add_argument("--remote-debugging-port=9222")  # Optional, useful for debugging
chrome_options.add_argument("--disable-gpu")  # Disables GPU acceleration
chrome_options.add_argument("--disable-software-rasterizer")  # Prevents Chrome from crashing in headless mode
chrome_options.add_argument("--window-size=1920x1080")  # Set the window size for headless mode
chromedriver_path = os.path.join(os.getcwd(), 'chromedriver')
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get("https://everynoise.com/")

# Set up db connection
def init_db():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("dbname"),
            user=os.getenv("user"),
            password=os.getenv("password"),
            host=os.getenv("host"),
            port=os.getenv("port")
        )
        print("Successfully connected to database.")
        return conn

    except:
        print("Failed connecting to database.")
        return None

def main(conn):
    # Record the start time
    start_time = time.time()

    # Scrape all genres + convert style attributes to DataFrame
    genres_elems = driver.find_elements(By.CLASS_NAME, "genre")

    # Initialize an empty list for genre data
    genres_objs = []

    # Function to scrape genre data (this will run in parallel threads)
    def scrape_genre(genre):
        genre_obj = {
            "genre": genre.get_attribute("innerText"),
            "preview_url": genre.get_attribute("preview_url"),
            "preview_track": re.sub(r'^e\.g\.\s*', '', genre.get_attribute("title"))
        }
        
        for style in genre.get_attribute("style").split(";")[:-1]:
            [key, value] = style.split(":")
            genre_obj[key.strip().replace("-", "_")] = re.sub(r'(px)$', '', value.strip())
        
        return genre_obj

    # Create a ThreadPoolExecutor for concurrent scraping
    with ThreadPoolExecutor(max_workers=4) as executor:
        # Use tqdm to display the progress
        futures = [executor.submit(scrape_genre, genre) for genre in genres_elems]
        
        # Use tqdm to monitor progress
        for future in tqdm(as_completed(futures), total=len(futures), desc="Scraping progress", unit="genre"):
            genres_objs.append(future.result())

    # Insert genres into database
    if conn:
        conn.cursor().executemany("""
            INSERT INTO genre (genre_name, preview_url, preview_track, color, top_pixel, left_pixel, font_size) 
            VALUES (%(genre)s, %(preview_url)s, %(preview_track)s, %(color)s, %(top)s, %(left)s, %(font_size)s);
        """, genres_objs)
        
        conn.commit()
    
    # Convert the list of genre objects to a DataFrame
    genres_df = pd.DataFrame(genres_objs)

    # Save data
    genres_df.to_csv(os.path.join(os.getcwd(), 'data', 'enao-genres.csv'), index=False)

    # Record the end time
    end_time = time.time()

    # Calculate elapsed time
    elapsed_time = end_time - start_time
    print(f"Scraping process completed in {elapsed_time:.2f} seconds.")

if __name__ == "__main__":
    conn = init_db()  
    while True:
        main(conn)
        time.sleep(300)