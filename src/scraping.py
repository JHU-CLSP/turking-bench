import time
import re
import os
from selenium import webdriver
from bs4 import BeautifulSoup

Page = 'https://workersandbox.mturk.com'

driver = webdriver.Firefox()
driver.get(Page)

# check if you are logged in
while (driver.title != 'Amazon Mechanical Turk'):
    time.sleep(5)

time.sleep(15)
html = driver.page_source

# Find the url of buttons
soup = BeautifulSoup(html, 'html.parser')
buttons = soup.find_all('a', class_=re.compile('btn work-btn'))
urls = [button['href'] for button in buttons]
for url in urls:
    new_url = Page + url
    driver.get(new_url)
    time.sleep(10)
    html_task = driver.page_source
    if not os.path.exists('turk_tasks/' + driver.title):
        os.makedirs('turk_tasks/' + driver.title)
    with open('turk_tasks/' + driver.title +'/' + 'template.html', 'w', encoding='utf-8') as f:
        f.write(html_task)
#    soup = BeautifulSoup(html_task, 'html.parser')
#    return_button = soup.find_all('a', class_=re.compile('btn btn-secondary'))

with open('page.html', 'w', encoding='utf-8') as f:
    f.write(html)

driver.close()