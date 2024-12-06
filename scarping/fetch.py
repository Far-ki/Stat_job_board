import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import random
import csv
import logging
import threading
import keyboard


chromedriver_autoinstaller.install()


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


stop_flag = False


def setup_driver():
    chrome_options = Options()
    chrome_options.binary_location = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
    chrome_options.add_argument("--log-level=3")
    return webdriver.Chrome(options=chrome_options)


def scroll_to_end(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    driver.execute_script("window.scrollBy(0, arguments[0]);", last_height)
    time.sleep(2)
    new_height = driver.execute_script("return document.body.scrollHeight")
    return last_height != new_height


def safe_find(driver, by, value, default="Brak danych"):
    try:
        return driver.find_element(by, value).text
    except Exception:
        return default


def extract_job_details(driver):
    try:
        details_xpath = {
            "type_of_work": "//*[@id='__next']/div[2]/div/div[1]/div/div[2]/div[2]/div[2]/div[1]/div[2]/div[2]",
            "experience": "//*[@id='__next']/div[2]/div/div[1]/div/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]",
            "employment_type": "//*[@id='__next']/div[2]/div/div[1]/div/div[2]/div[2]/div[2]/div[3]/div[2]/div[2]",
            "operating_mode": "//*[@id='__next']/div[2]/div/div[1]/div/div[2]/div[2]/div[2]/div[4]/div[2]/div[2]",
        }
        details = {key: safe_find(driver, By.XPATH, value) for key, value in details_xpath.items()}
        
        description = " ".join(desc.text for desc in driver.find_elements(By.XPATH, "//div[@class='MuiBox-root css-tbycqp']//ul//li"))
        
        return {
            "title": safe_find(driver, By.CSS_SELECTOR, "h1", "Brak tytułu"),
            "city": safe_find(driver, By.CLASS_NAME, "css-1o4wo1x", "Brak miasta"),
            "description": description,
            **details,
            "url": driver.current_url
        }
    except Exception as e:
        logger.error(f"Error extracting job details: {e}")
        return {}

def save_to_csv(data, filename="oferty_pracy.csv"):
    with open(filename, mode='w', newline='', encoding='utf-8') as plik:
        naglowki = ["id", "title", "city", "type_of_work", "experience", "employment_type", "operating_mode", "description", "url"]
        writer = csv.DictWriter(plik, fieldnames=naglowki)
        writer.writeheader()
        writer.writerows(data)


def stop_program():
    global stop_flag
    logger.info("Naciśnij ESC, aby zatrzymać działanie programu.")
    keyboard.wait("esc")
    stop_flag = True
    logger.info("Program został zatrzymany przez użytkownika.")

def scrape_jobs():
    global stop_flag
    driver = setup_driver()
    try:
        driver.get("https://justjoin.it/")
        time.sleep(5)

        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            });
            """
        })

        try:
            accept_cookie_button = driver.find_element(By.ID, "cookiescript_accept")
            accept_cookie_button.click()
        except Exception:
            logger.info("Brak przycisku do akceptacji ciasteczek.")

        data = []
        current_index = 0

        while not stop_flag:
            try:
                element_xpath = f"//div[@data-index='{current_index}']"
                element = driver.find_element(By.XPATH, element_xpath)
                action = ActionChains(driver)
                action.move_to_element_with_offset(element, 0, 50).click().perform()
                time.sleep(random.uniform(1.5, 3.5))

                oferta = extract_job_details(driver)
                oferta["id"] = current_index
                data.append(oferta)

                logger.info(f"Pobrano ofertę: {oferta['title']} ({current_index})")
                driver.back()
                time.sleep(random.uniform(1.5, 3.5))

                current_index += 1
            except Exception as e:
                logger.error(f"Nie odnaleziono elementu data-index={current_index}: {e}")
                if not scroll_to_end(driver) or stop_flag:
                    logger.info("Dotarto do końca strony lub zatrzymano program.")
                    break

        save_to_csv(data)
        logger.info(f"Zapisano {len(data)} ofert do pliku CSV.")

    except Exception as e:
        logger.error(f"Błąd główny: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    threading.Thread(target=stop_program, daemon=True).start()
    scrape_jobs()
