from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import json

def setup_driver():

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()),
                             options= options)
    
    return driver

def save_cookies():
    driver = setup_driver()

    # Go to the Harvard Recreation login page
    driver.get("https://membership.gocrimson.com")

    print("\n=== MANUAL LOGIN REQUIRED ===")
    print("1. Log in fully with HarvardKey.")
    print("2. Approve DUO.")
    print("3. Wait until you see your dashboard/homepage.")
    print("4. Then return here and press Enter.\n")
    input("Press Enter ONLY after the dashboard has fully loaded: ")

    # Save cookies
    cookies = driver.get_cookies()

    with open("cookies.json", "w") as f:
        json.dump(cookies, f)

    print("\nCookies saved successfully → cookies.json")
    driver.quit()

if __name__ == "__main__":
    save_cookies()