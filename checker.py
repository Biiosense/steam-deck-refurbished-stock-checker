from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import requests
import logging 
from datetime import datetime

# Configurations
webhook_url = "https://discord.com/api/webhooks/1392809397280964740/zJwaI96qRjZNrPmPRZGmR63XJwJ9bS9TDtE79LnkWp9CyyNOwCNW9abATHGqJTSJ8LUq"
page_url = "https://store.steampowered.com/sale/steamdeckrefurbished/" 
debug = False # Set to True to always send a notification with a screenshot

# Set up Selenium WebDriver options
options = Options()
options.add_argument('--headless')  # Run in headless mode
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
service = Service("/usr/bin/chromedriver")  # Update with the correct path to your ChromeDriver

## Setup logging
logging.basicConfig(
    filename='/home/Max/GitHome/steam-deck-refurbished-stock-checker/steamdeck.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%D %H:%M:%S'
)

# Start WebDriver
driver = webdriver.Chrome(service=service, options=options)
try:
    try:
        driver.get(page_url)
    except Exception as e:
        logging.info("Erreur lors du chargement de la plage: %s", page_url);
        raise

    # Wait for page to load dynamic content
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "ImpressionTrackedElement")))
    time.sleep(10)  # Extra wait to ensure all dynamic content is fully loaded

    # Set the window size to capture the full page
    driver.set_window_size(1920, 1500)

    # Check for "Out of stock" occurrences
    page_source = driver.page_source
    add_to_cart_count = page_source.lower().count("add to cart")

    # Prepare screenshot archive directory
    archive_dir = '/home/Max/GitHome/steam-deck-refurbished-stock-checker/screenshots'
    os.makedirs(archive_dir, exist_ok=True)

    # Register name of the screenshot
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    screenshot_path = os.path.join(archive_dir, f"steamdeck_{timestamp}.png")

    # Take a full-page screenshot
    driver.save_screenshot(screenshot_path)

    # Determine if a notification should be sent
    if (add_to_cart_count > 0) or debug:
        logging.info("Steam Deck reconditionné en stock!")
        message = {
            "content": f"Steam Deck reconditionné en stock!",
        }
        files = {
            "file": ("screenshot.png", open(screenshot_path, "rb"))
        }
        response = requests.post(webhook_url, data=message, files=files)
    else:
        logging.info("Pas de Steam Deck reconditionné en stock!\nPas de notification")
        if os.path.exists(screenshot_path):
            os.remove(screenshot_path)

except Exception as e:
    logging.exception("Une erreur inattendue est survenue: ")

finally:
    driver.quit()


