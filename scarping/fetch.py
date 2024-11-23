import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import random
import csv


chromedriver_autoinstaller.install()

chrome_options = Options()
chrome_options.binary_location = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
chrome_options.add_argument("--log-level=3")

driver = webdriver.Chrome(options=chrome_options)

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

    accept_cookie_button = driver.find_element(By.ID, "cookiescript_accept")
    accept_cookie_button.click()

    last_index = -1
    current_index = 0
    if_offer = 0
    data = []

    while True:
        try:
            element_xpath = f"//div[@data-index='{current_index}']"
            element = driver.find_element(By.XPATH, element_xpath)
            action = ActionChains(driver)
            action.move_to_element_with_offset(element, 0, 50).click().perform()
            time.sleep(random.uniform(1.5, 3.5))

            try:
                Title = driver.find_element(By.CSS_SELECTOR, "h1").text
                City = driver.find_element(By.CLASS_NAME, "css-1o4wo1x").text
                Type_of_work = driver.find_element(By.XPATH, "//*[@id='__next']/div[2]/div/div[1]/div/div[2]/div[2]/div[2]/div[1]/div[2]/div[2]").text
                Experience = driver.find_element(By.XPATH, "//*[@id='__next']/div[2]/div/div[1]/div/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]").text
                Employment_type = driver.find_element(By.XPATH, "//*[@id='__next']/div[2]/div/div[1]/div/div[2]/div[2]/div[2]/div[3]/div[2]/div[2]").text
                Operating_mode = driver.find_element(By.XPATH, "//*[@id='__next']/div[2]/div/div[1]/div/div[2]/div[2]/div[2]/div[4]/div[2]/div[2]").text
                description_elements = driver.find_elements(By.XPATH, "//div[@class='MuiBox-root css-tbycqp']//ul//li")
                description = " ".join([desc.text for desc in description_elements]) 

            except Exception as e:
                print(f"Nie odnaleziono wszystkich elementów oferty: {e}")
                Title = "Brak tytułu"
                City = "Brak miasta"
                Type_of_work = "Brak typu pracy"
                Experience = "Brak doświadczenia"
                Employment_type = "Brak danych o rodzaju zatrudnienia"
                Operating_mode = "Brak typu pracy"
                description = "Brak opisu" 

            oferta = {
                "id": if_offer,
                "title": Title,
                "city": City,
                "type_of_work": Type_of_work,
                "experience": Experience,
                "employment_type": Employment_type,
                "operating_mode": Operating_mode,
                "description": description 
            }
            data.append(oferta)
            if_offer += 1

            driver.back()
            time.sleep(random.uniform(1.5, 3.5))

            element = driver.find_element(By.CSS_SELECTOR, "div")
            ActionChains(driver).move_to_element_with_offset(
                element, random.randint(-10, 10), random.randint(-10, 10)
            ).perform()
            time.sleep(random.uniform(1, 3))

            current_index += 1

        except Exception as e:
            print(f"Nie znaleziono elementu data-index={current_index}. Przewijanie w dół...")


            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
            time.sleep(3)
            print(data)
            print(f"current_index: {current_index}, last_index: {last_index}")
            if current_index == last_index:

                with open('oferty_pracy.csv', mode='w', newline='', encoding='utf-8') as plik:
                    naglowki = ["id", "title", "city", "type_of_work", "experience", "employment_type", "operating_mode", "description"]
                    writer = csv.DictWriter(plik, fieldnames=naglowki)
                    writer.writeheader()
                    writer.writerows(data)
                break
            last_index = current_index

except Exception as e:
    print("Wystąpił błąd główny:", e)
    with open('oferty_pracy.csv', mode='w', newline='', encoding='utf-8') as plik:
        naglowki = ["id", "title", "city", "type_of_work", "experience", "employment_type", "operating_mode", "description"]
        writer = csv.DictWriter(plik, fieldnames=naglowki)
        writer.writeheader()
        writer.writerows(data)
finally:
    driver.quit()
