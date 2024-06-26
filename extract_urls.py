from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
import os
import mysql.connector
from mysql.connector import Error

# Initialize Selenium WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Function to perform a Google search
def perform_google_search(query):
    driver.get("https://www.google.com")
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(query)
    search_box.submit()

# Function to extract URLs from search results
def extract_urls(max_urls=1000):
    urls = []
    pages_visited = 0
    while len(urls) < max_urls:
        time.sleep(2)  # Wait for the page to load
        results = driver.find_elements(By.XPATH, "//a[@href]")
        for result in results:
            url = result.get_attribute("href")
            if "arcgis/rest/services" in url:
                urls.append(url)
                if len(urls) >= max_urls:
                    break
        try:
            next_button = driver.find_element(By.ID, "pnnext")
            next_button.click()
            pages_visited += 1
        except:
            break  # No more pages or "Next" button not found

        # Optional: Add additional logic for handling rate limiting or captchas

    return urls[:max_urls]  # Ensure we return exactly max_urls

# Perform the search and extract URLs
query = "arcgis/rest/services"
perform_google_search(query)
urls = extract_urls(max_urls=1000)
driver.quit()

# Save URLs to CSV, appending to existing file if it exists
def save_to_csv(urls, filename="arcgis_urls_accumulated.csv"):
    if os.path.exists(filename):
        df_existing = pd.read_csv(filename)
        existing_urls = set(df_existing["URL"])
        urls = list(set(urls).union(existing_urls))
    
    df = pd.DataFrame(urls, columns=["URL"])
    df.to_csv(filename, index=False)

# Save URLs to CSV (optional)
save_to_csv(urls)

# Function to save URLs to MySQL database
def save_to_mysql(urls):
    try:
        connection = mysql.connector.connect(
            host='localhost',  # Change this to your MySQL host
            database='arcgis_urls_db',  # Name of your MySQL database
            user='root',  # MySQL username
            password='root'  # MySQL password
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # Insert URLs into MySQL table
            for url in urls:
                query = "INSERT INTO arcgis_urls (url) VALUES (%s)"
                cursor.execute(query, (url,))
            
            connection.commit()
            print(f"{len(urls)} URLs inserted into MySQL database successfully.")

    except Error as e:
        print(f"Error inserting data into MySQL table: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed.")

# Call the function to save URLs to MySQL
save_to_mysql(urls)
