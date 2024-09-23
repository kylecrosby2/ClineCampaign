#! python3
# GoogleNewsScraper.py - Scrapes Google News for articles based on a search query, and then copies their text into a
# text file.

import requests
import webbrowser
import bs4
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import pyperclip


def main():
    PATH = "C:\Program Files (x86)\chromedriver.exe"
    driver = webdriver.Chrome(PATH)
    driver.get('https://www.google.com/search?rlz=1C1CHBF_enUS909US909&biw=1360&bih=625&tbm=nws&sxsrf=ALeKk01UjrNYZ8W1Bo95qair56KYP6Uo9g%3A1598204258002&ei=YalCX9btPPygytMP0dOQ4Ag&q=david+mckinley+west+virginia&oq=david+mckinley+west+virginia&gs_l=psy-ab.3..33i299k1.7971.10033.0.10146.14.14.0.0.0.0.129.1120.13j1.14.0....0...1c.1.64.psy-ab..0.14.1119....0.yTnr-w33qoE')
    page_url = driver.current_url
    link_elems = driver.find_elements_by_class_name("dbsr")
    os.mkdir('C:/Users/kerry/Documents/NatalieClineDocuments/NewsArticles')
    index = 0
    for i in range(len(link_elems)):
        link_elems2 = driver.find_elements_by_class_name("dbsr")
        index +=1
        link_elems2[i].click()
        body = driver.find_element_by_css_selector('body')
        body.send_keys(Keys.CONTROL + 'a')
        body.send_keys(Keys.CONTROL + 'c')
        text = pyperclip.paste()
        file = open('C:/Users/kerry/Documents/NatalieClineDocuments/NewsArticles/Article' + str(index) + '.txt', 'w')
        file.write(text)
        file.close()
        time.sleep(0.2)
        driver.get(page_url)
        time.sleep(0.2)
    #next_page_elem = driver.find_elements_by_class_name("G0iuSb")
    #next_page_elem[0].click()
    #time.sleep(4)



def get_urls():
    PATH = "C:\Program Files (x86)\chromedriver.exe"
    driver = webdriver.Chrome(PATH)
    driver.get(
        'https://www.google.com/search?q=david+mckinley+west+virginia&rlz=1C1CHBF_enUS909US909&tbm=nws&sxsrf=ALeKk02fWiCRBRMNA1PvGSMAQ8EFh7yJ8w:1598204268678&source=lnt&tbs=qdr:y&sa=X&ved=0ahUKEwiN6Nnt7rHrAhWMoHIEHSnWBUUQpwUIJA&biw=1360&bih=625&dpr=1')
    url_list = []
    link_elems = driver.find_elements_by_class_name("dbsr")
    for j in range(2):
        page_url = driver.current_url
        for i in range(len(link_elems)):
            link_elems2 = driver.find_elements_by_class_name("dbsr")
            link_elems2[i].click()
            url = driver.current_url
            l = url.split('/')
            url_list.append(l[2])
            driver.get(page_url)
        next_page_elem = driver.find_elements_by_class_name("G0iuSb")
        next_page_elem[0].click()
    clicked = []
    occur_list = []
    for i in url_list:
        if i not in clicked:
            occurrences = url_list.count(i)
            occur_list.append((occurrences, str(i)))
            clicked.append(i)
    occur_list.sort()
    occur_list.reverse()
    for i in occur_list:
        print(i)


get_urls()
