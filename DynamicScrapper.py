from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import json

# List of page paths 
page_paths = ["welcome","signin","dashboard"]  

# login credentials
email = "email"
password = "password"

# Webdriver
driver = webdriver.Chrome()

# Function to scroll down to load more content
def scroll_to_load(driver, scroll_pause_time=2, scrolls=10):
    print("Starting to scroll and load more content...")
    for _ in range(scrolls):
        # Scroll down to the bottom of the page
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
        # Wait for new content to load
        time.sleep(scroll_pause_time)
    print(f"Completed {scrolls} scrolls.")

# Function to clean the text and generate keys
def generate_key(text):
    print(f"Generating key for the text: {text[:50]}...")  
    return text.strip().replace(" ", "_").replace("\n", "_").replace("\r", "").replace("-", "_").capitalize()

# Function to log in automatically
def login_if_required(driver):
    try:
        # Check if the login page is loaded
        email_field = driver.find_element(By.ID, "login_email_input")
        password_field = driver.find_element(By.ID, "login_password_input")

        print("Login page detected. Logging in...")

        # Enter the email and password
        email_field.send_keys(email)
        password_field.send_keys(password)

        # Submit the form 
        password_field.send_keys(Keys.RETURN)
        
        print("Login submitted.")
        time.sleep(3) 

    except Exception as e:
        print("Login page not detected or already logged in:", e)

# Loop through each page path in the list
for path in page_paths:
    print(f"Processing page: {path}")
    url = f"http://localhost:5173/{path}"
    driver.get(url)
    print(f"Navigating to URL: {url}")

    # login function if needed
    login_if_required(driver)

    # Scroll to load more content
    scroll_to_load(driver, scroll_pause_time=2, scrolls=10)

    # Extract all visible text on the page
    texts = driver.find_elements(By.XPATH, "//*[not(self::script or self::style)]")  
    print(f"Extracted {len(texts)} text elements from the page.")

    data = {}

    for text_element in texts:
        text = text_element.text.strip()
        if text:  # Only process non-empty text
            key = generate_key(text)
            data[key] = text
            print(f"Added key: {key} with text length: {len(text)}")

    # Save the data as a JSON file with the page path name
    filename = f"json/{path}.json"
    print(f"Saving data to {filename}...")
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

    print(f"All visible text data for {path} has been saved to {filename}")

# Close the Selenium browser
driver.quit()
print("Selenium browser has been closed.")
