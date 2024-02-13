from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from io import BytesIO
from PIL import Image

display = Display(visible=0, size=(800, 600))
display.start()

options = Options()

browser = webdriver.Chrome(options=options)
browser.get('http://www.google.com')
browser.save_screenshot('screenshots/screenie.png')
# screenshot = browser.get_screenshot_as_png()
# image = Image.open(BytesIO(screenshot))
browser.quit()

display.stop()