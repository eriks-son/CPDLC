from bs4 import BeautifulSoup
from selenium import webdriver
import time


def get_track(departure: str, arrival: str):
    browser = webdriver.Chrome()
    browser.get(f"https://skyvector.com/?ll=&fpl=%20{departure}%20undefined%20{arrival}")
    html = browser.page_source
    time.sleep(2)
    browser.close()

    soup = BeautifulSoup(html, features='lxml')
    g = soup.find_all('g')
    text_element = g[-1].find_next('text')[0]
    track = text_element.text.partition('°')[0]
    return track


print(get_track("KEWR", "KIND"))
