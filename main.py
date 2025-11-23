from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import time
import json
import datetime
from emailer import send_email
import os


def setup_driver():

    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")      # run Chrome in background
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    options.binary_location = os.environ.get("CHROME_BIN", "/usr/bin/chromium")

    driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()),
                             options= options)
    
    return driver


def parse_into_text(day, month, year):
    hash = {0: 'JANUARY', 1: 'FEBRUARY', 2: 'MARCH', 3: 'APRIL', 4: 'MAY', 5: 'JUNE', 
            6: 'JULY', 7: 'AUGUST', 8: 'SEPTEMBER', 9: 'OCTOBER', 10: 'NOVEMBER', 11: 'DECEMBER'}
    
    weekday = datetime.date(year, month + 1, day).strftime("%A")

    

    return f"{weekday.upper()}, {hash[month]} {day}, {year}"
    


def click_button(driver):
    wait = WebDriverWait(driver, 5)

    try:
        btn = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button.selectDateBtn.single-date-select-button")
            )
        ) 

        driver.execute_script("""
                        var evt = new MouseEvent('click', {bubbles: true, cancelable: true, view: window});
                            arguments[0].dispatchEvent(evt);
                        """, btn)

        time.sleep(0.3)

        print("Clicked Select Date button.")
        return True

    except:
        print("Select Date button not clickable — skipping.")
        return False
    

def check_availability(driver, date_list):
    driver.refresh()

    time.sleep(1) 

    button_present = click_button(driver)

    if button_present:
        time.sleep(2)

        cells = driver.find_elements(
                    By.CSS_SELECTOR,
                    "td.current-month.gj-cursor-pointer"
                )

       
        for cell in cells:
            day   = int(cell.get_attribute("day"))
            month = int(cell.get_attribute("month"))
            year  = int(cell.get_attribute("year"))

            exact_date = parse_into_text(day, month, year)
    
            if exact_date in date_list:
                return exact_date
            
        return None
    
    else:
        
        spans = driver.find_elements(By.CSS_SELECTOR, "span.sr-only")
        texts = [s.text.strip() for s in spans]

        for text in texts:
            if text.upper() in date_list:
                return text

        return None

    

def main():
    driver = setup_driver()

    dates = set() # empty for now
    with open('dates.txt', 'r') as f:
        for date in f.read().split('\n'):
            dates.add(date)

    calendar = "https://membership.gocrimson.com/Program/GetProgramDetails?courseId=3b92dfe2-3eb0-4860-b07f-f058e0e18019"

    driver.get(calendar)
    time.sleep(5)
    
    available_day = None

    days_checked = set()
    
    while True:
        try:
            available_day = check_availability(driver, dates)

            if available_day and available_day not in days_checked:
                send_email(
                    subject=f"Court Available! {available_day}",
                    body=f"Good news. A court is now available at the following date: {available_day}",
                    to_email="gabrieltimoteo@college.harvard.edu"
                )

                dates.remove(available_day)
                days_checked.add(available_day)

                # save updated dates file (rewrite everything)
                with open("dates.txt", "w") as f:
                    for d in dates:
                        f.write(d + "\n")

            print("Checked. Sleeping for 120 seconds...")
            time.sleep(120)

        except Exception as e:
            print("Error in loop:", e)
            time.sleep(10)
        

if __name__ == "__main__":
    main()