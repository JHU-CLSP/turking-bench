from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pyvirtualdisplay import Display

display = Display(visible=0, size=(1920, 1080))
display.start()

options = Options()

driver = webdriver.Chrome(options=options)
str1 = driver.capabilities['browserVersion']
str2 = driver.capabilities['chrome']['chromedriverVersion'].split(' ')[0]
print(f"browserVersion {str1}")
print(f"chromedriverVersion {str2}")

display.stop()
driver.quit()