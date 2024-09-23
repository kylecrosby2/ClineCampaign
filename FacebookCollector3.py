#! python3
# This program was just a test of a feature of the collector.


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pyperclip
import time
import re


def main():
    PATH = "C:\Program Files (x86)\chromedriver.exe"
    driver = webdriver.Chrome(PATH)
    driver.get('https://www.facebook.com/pg/RepMcKinley/posts/?ref=page_internal')
    html_elem = driver.find_element_by_tag_name("body")
    if 'August 8' in html_elem.text:
        print('found it')
    else:
        print("didn't find it")


main()
