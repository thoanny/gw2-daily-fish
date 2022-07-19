import requests
from os import getcwd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# Open template to get content
with open('tpl.html', encoding="utf-8") as template:
    tpl = template.read()
template.close()

# Get data JS from repository
url = "https://raw.githubusercontent.com/thoanny/fishing-companion/main/src/js/_maps.js"
maps = requests.get(url)
with open("maps.js", "wb") as file:
    content = maps.content.replace(b'export const maps', b'const maps')
    file.write(content)

# Get daily fish from repository
url = "https://raw.githubusercontent.com/thoanny/fishing-companion/main/daily.txt"
daily = requests.get(url)
daily = daily.text.rstrip().split(',')
fish = daily[-1]

# Get fish data from GW2 API
url = "https://api.guildwars2.com/v2/items/%s?lang=fr" % fish
api = requests.get(url)
fish = api.json()

fishIcon = requests.get(fish['icon'])
with open("icon.png", "wb") as file:
    file.write(fishIcon.content)

# Then, let the magic happen!
tpl = tpl.replace('%%RARITY%%', fish['rarity'])
tpl = tpl.replace('%%FISH%%', str(fish['id']))

f = open('fish.html', 'w+', encoding='utf-8')
f.write(tpl)
f.close()

options = webdriver.ChromeOptions()
options.headless = True
s = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s, options=options)
driver.maximize_window()
driver.implicitly_wait(3)

fish = getcwd() + "\\fish.html"

driver.get("file:///" + fish)

driver.fullscreen_window()

S = lambda X: driver.execute_script('return document.body.parentNode.scroll' + X)
driver.set_window_size(S('Width'), S('Height'))
driver.find_element(By.TAG_NAME, 'body').screenshot(f'daily-fish.png')

driver.quit()
