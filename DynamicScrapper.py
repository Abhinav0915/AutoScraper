from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import json

# List of page paths 
page_paths = ["welcome", "usecases", "allServices","ProdigiDesk","signin","signup", ]  

#Webdriver
driver = webdriver.Chrome()

# Function to scroll down to load more content
def scroll_to_load(driver, scroll_pause_time=2, scrolls=5):
    for _ in range(scrolls):
        # Scroll down to the bottom of the page
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
        # Wait for new content to load
        time.sleep(scroll_pause_time)

# Function to clean the text and generate keys
def generate_key(text):
    return text.strip().replace(" ", "_").replace("\n", "_").replace("\r", "").replace("-", "_").capitalize()

# Loop through each page path in the list
for path in page_paths:
    url = f"https://prodigidesk.ai/{path}"
    driver.get(url)

    # Scroll to load more content
    scroll_to_load(driver, scroll_pause_time=2, scrolls=10)

    # Extract all visible text on the page
    texts = driver.find_elements(By.XPATH, "//*[not(self::script or self::style)]")  

    data = {}

    for text_element in texts:
        text = text_element.text.strip()
        if text:  # Only process non-empty text
            key = generate_key(text)
            data[key] = text

    # Save the data as a JSON file with the page path name
    filename = f"json/{path}.json"
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

    print(f"All visible text data for {path} has been saved to {filename}")

# Close the Selenium browser
driver.quit()
