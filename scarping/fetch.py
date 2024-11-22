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

driver = webdriver.Chrome(options=chrome_options)

try:
    driver.get("https://justjoin.it/")
    print("Otwarta strona:", driver.title)
    time.sleep(5)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
    Object.defineProperty(navigator, 'webdriver', {
      get: () => undefined
    });
    """
})

    accept_cookie_button = driver.find_element(By.ID,"cookiescript_accept")
    accept_cookie_button.click()
    last_index = -1
    current_index = 0
    if_offer =0
    data = []
    while True:
        try:

            element_xpath = f"//div[@data-index='{current_index}']"
            element = driver.find_element(By.XPATH, element_xpath)
            print(f"Kliknięcie w element data-index={current_index}")

            action = ActionChains(driver)
        
            action.move_to_element_with_offset(element, 0, 50).click().perform() 
            
           
            time.sleep(random.uniform(1.5, 3.5))

            try:
                h1_element = driver.find_element(By.CSS_SELECTOR, "h1")
                print(f"Znaleziony tekst w h1 to: {h1_element.text}")
            except Exception as e:
                print("Nie znaleziono elementu h1 na stronie", e)

            print(f"Pobrano szczegóły dla elementu data-index={current_index}")

            oferta = {
                "id": if_offer,
                "title": h1_element.text
            }
            data.append(oferta)
            if_offer+= 1


            driver.back()
            time.sleep(random.uniform(1.5, 3.5))
            element = driver.find_element(By.CSS_SELECTOR, "div")
            ActionChains(driver).move_to_element_with_offset(element, random.randint(-10, 10), random.randint(-10, 10)).perform()
            time.sleep(random.uniform(1, 3))

            current_index += 1

        except Exception as e:
            print(f"Nie znaleziono elementu data-index={current_index}. Przewijanie w dół...")

            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
            time.sleep(3) 

            if current_index == last_index:
                print("Koniec elementów na stronie.")
                
                break
            last_index = current_index
    
except Exception as e:
    print("Wystąpił błąd:", e)
    with open('oferty_pracy.csv', mode='w', newline='', encoding='utf-8') as plik:
        naglowki = ["id", "title"]
        writer = csv.DictWriter(plik, fieldnames=naglowki)
        writer.writeheader()
        writer.writerows(data)

finally:
    driver.quit()
