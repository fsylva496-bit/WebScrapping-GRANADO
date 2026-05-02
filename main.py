from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from fake_useragent import UserAgent
import time

options = Options()
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('prefs', {'profile.managed_default_content_settings.media_stream': 2})
options.add_argument('--start-maximized')
options.add_argument('--disable-infobars')
#options.add_argument('--disable-extensions')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
options.add_argument('--window-size=1920,1200')
options.add_argument('--start-fullscreen')
options.add_argument('--mute-audio')
options.add_extension('./ublock.crx')
options.add_argument('--blink-settings=imagesEnabled=false')
options.add_argument('--disable-notifications')
options.add_argument('--disable-features=PreloadMediaEngagementData,MediaEngagementBypassAutoplayPolicies')
options.add_argument('--autoplay-policy=user-required')
ua = UserAgent()
user_agent = ua.random
options.add_argument(f"user-agent={user_agent}")

monpilote = webdriver.Chrome(options=options)
print('Chrome démarré')

monpilote.get("https://www.granado.eu/fr/")

monbouton = WebDriverWait(monpilote, timeout=3).until(expected_conditions.element_to_be_clickable((By.XPATH,"/html/body/div[1]/div[1]/div/div[1]/div[3]/div/button[3]")))
monbouton.click()

monbouton = WebDriverWait(monpilote, timeout=3).until(expected_conditions.element_to_be_clickable((By.XPATH,"/html/body/div[3]/header/div[2]/div[3]/div[1]")))
monbouton.click()

produit = 'parfums'

mazone= monpilote.find_element(By.XPATH, '/html/body/div[3]/header/div[2]/div[3]/div[2]/div[1]/div[3]/form/div[2]/input' )

mazone.send_keys(produit)
mazone.send_keys(Keys.ENTER)

monbouton = WebDriverWait(monpilote, timeout=3).until(expected_conditions.element_to_be_clickable((By.XPATH,'//*[@id="algolia-sorts"]/div')))
monbouton.click()

monbouton = WebDriverWait(monpilote, timeout=3).until(expected_conditions.element_to_be_clickable((By.XPATH,'//*[@id="algolia-sorts"]/div/select')))
monbouton.click()

#listeDeroul = WebDriverWait(monpilote, timeout=3).until(expected_conditions.presence_of_element_located((By.XPATH,'//*[@id="algolia-sorts"]/div/select')))
#Select(listeDeroul).select_by_visible_text('Prix plus bas')  n'a pas marché

zoneNom = WebDriverWait(monpilote, timeout=3).until(expected_conditions.presence_of_element_located((By.XPATH,'//*[@id="maincontent"]/div[2]/h1')))

Nom = zoneNom.text
print('Nom:', Nom)

time.sleep( 0.5 ) 

listParfums = []

ParfumsPages = WebDriverWait(monpilote, timeout=10).until(expected_conditions.presence_of_all_elements_located((By.XPATH,'//*[@id="instant-search-results-container"]/div/ol/li[*]/div/div/div[1]/div[2]/div[3]/h3/a')))

for x in ParfumsPages:
  Parfums = x.text
  listParfums.append( Parfums )
  print(len(listParfums), Parfums)

listPrix = []

PrixPages = WebDriverWait(monpilote, timeout=10).until(expected_conditions.presence_of_all_elements_located((By.XPATH,'//*[@id="instant-search-results-container"]/div/ol/li[*]/div/div/div[1]/div[2]/div[3]/div[1]/div/div/div/div/span')))

for x in PrixPages:
  Prix = x.text
  listPrix.append( Prix )
  print(len(listPrix), Prix)

time.sleep( 0.5 ) 

a = []
a.append(['Parfums', 'Prix'])
for i in range(len(listParfums)):
    Parfums = listParfums[i]
    Prix = listPrix[i]
    a.append([Parfums, Prix])

print (a)

import csv
fichier = open( "granado.csv" , "w" )
écrivain = csv.writer( fichier , delimiter="," )
écrivain.writerows( a  )
fichier.close()

input("Presser une touche pour quitter...")