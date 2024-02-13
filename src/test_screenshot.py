from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

display = Display(visible=0, size=(1920, 1080))
display.start()

options = Options()

browser = webdriver.Chrome(options=options)
browser.get('http://www.google.com')
browser.save_screenshot('screenshots/screenie.png')
browser.quit()

display.stop()