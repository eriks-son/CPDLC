from bs4 import BeautifulSoup
from selenium import webdriver
import time


# THIS IS UNUSED IN THE PROJECT
# IT OPENS A CHROME WINDOW THEN FINDS THE TRACK BETWEEN THE AIRPORTS
# THIS WAS VERY INEFFICIENT AND INCONSISTENT
# THE airport_database.dat IS MUCH QUICKER AND WORKS FOR ALL MAJOR AIRPORTS ALL AROUND THE WORLD
# IT ONLY LACKS SMALL AIRPORTS THAT WILL NOT HAVE PREFERRED ROUTES ANYWAYS


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
