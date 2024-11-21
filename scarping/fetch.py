import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


chromedriver_autoinstaller.install()

chrome_options = Options()
chrome_options.binary_location = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe" 


driver = webdriver.Chrome(options=chrome_options)

driver.get("https://justjoin.it/")
print(driver.title)
driver.quit()
