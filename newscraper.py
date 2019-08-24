import argparse, urllib.parse, hashlib
from datetime import timedelta, datetime 
from pymongo import MongoClient
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
from bs4 import BeautifulSoup

def changePage(browser,page):
    try:
        browser.get(page)
    except:
        return None
    return browser.title

def getPosts(browser,pagina):
    soup = BeautifulSoup(browser.find_element_by_tag_name('body').get_attribute("innerHTML"), 'html.parser')
    anchors = soup.find_all("a")
    for anchor in anchors:
        anchor_text = anchor.get_text()
        if len(anchor_text.split()) > 1:
            collectedUTC = datetime.utcnow().strftime("%d/%m/%Y-%H:%M:%S")
            # md5 = hashlib.md5(anchor_text.encode()) 
            # md5.hexdigest()
            if anchor.has_attr('title'):
                news.insert_one({
                    "parent":       pagina,
                    "collectedUTC": collectedUTC,
                    "href":         anchor.get('href'),
                    "title":        anchor.get('title'),
                    "text":         anchor_text,
                    "innerHTML":    anchor.decode_contents(formatter="html")
                })
            else:
                news.insert_one({
                    "parent":       pagina,
                    "collectedUTC": collectedUTC,
                    "href":         anchor.get('href'),
                    "text":         anchor_text,
                    "innerHTML":    anchor.decode_contents(formatter="html")
                })            
        
if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description='Global News Scraper')
    # parser.add_argument('delay', help='Delay')
    # args = parser.parse_args()
    client = MongoClient("mongodb://localhost:27017")
    db = client['news']
    sources = db['sources']
    news = db['news']

    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    chrome_options.add_experimental_option("prefs",prefs)
    chrome_options.add_argument('log-level=3')
    # chrome_options.add_argument('--proxy-server=46.102.106.37:13228') # PROXY

    browser = webdriver.Chrome(chrome_options=chrome_options)

    fontes = sources.find({})
    for fonte in fontes:
        pagina = fonte['url']
        if changePage(browser,pagina):
            sources.find_and_modify(query={'url':pagina}, update={"$inc": {'views': 1}}, upsert=False, full_response= True)
            getPosts(browser,pagina)
        else:
            sources.find_and_modify(query={'url':pagina}, update={"$set": {'status': "unreachable"}}, upsert=False, full_response= True)
 
    browser.stop_client()
    browser.quit()