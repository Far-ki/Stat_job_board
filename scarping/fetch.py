import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time

chromedriver_autoinstaller.install()

chrome_options = Options()
chrome_options.binary_location = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"

driver = webdriver.Chrome(options=chrome_options)

try:
    driver.get("https://justjoin.it/")
    print("Otwarta strona:", driver.title)
    time.sleep(5)
   
    accept_cookie_button = driver.find_element(By.ID,"cookiescript_accept")
    accept_cookie_button.click()
    last_index = -1
    current_index = 0
    while True:
        try:

            element_xpath = f"//div[@data-index='{current_index}']"
            element = driver.find_element(By.XPATH, element_xpath)
            print(f"Kliknięcie w element data-index={current_index}")

            action = ActionChains(driver)
        
            action.move_to_element_with_offset(element, 0, 50).click().perform() 
            
           
            time.sleep(2)

            try:
                h1_element = driver.find_element(By.CSS_SELECTOR, "h1")
                print(f"Znaleziony tekst w h1 to: {h1_element.text}")
            except Exception as e:
                print("Nie znaleziono elementu h1 na stronie", e)

            print(f"Pobrano szczegóły dla elementu data-index={current_index}")

            driver.back()
            time.sleep(2)

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

finally:
    driver.quit()
