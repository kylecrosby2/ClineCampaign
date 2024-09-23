#! python3
# FacebookCollector2.py -- Second try at the Facebook Collector


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pyperclip
import time
import re
import os


def main():
    start_time = time.time()
    PATH = "C:\Program Files (x86)\chromedriver.exe"
    driver = webdriver.Chrome(PATH)
    driver.get('https://www.facebook.com/pg/RepMcKinley/posts/?ref=page_internal')
    html_elem = driver.find_element_by_tag_name("body")
    scrolling = True
    copy_num = 0
    while scrolling:
        #loop_start_time = time.time()
        #copy_num += 1
        for i in range(80):
            html_elem.send_keys(Keys.PAGE_DOWN)
        # 100 to May 12: 97.2
        # 80 to May 12: 92.8
        # 50 to May 12: 117
        # 65 to May 12: 117
        #d = copy_num/60
        #if d.is_integer() is True or time.time() - loop_start_time > 60:
            #if 'January 19, 2011' in html_elem.text or 'January 18, 2011' in html_elem.text or 'January 17, 2011' in html_elem.text or 'January 20, 2011' in html_elem.text:
                #scrolling = False
    if scrolling is False:
        body = driver.find_element_by_css_selector('body')
        body.send_keys(Keys.CONTROL + 'a')
        body.send_keys(Keys.CONTROL + 'c')
        text = str(pyperclip.paste())
        text = deEmojify(text)
        file = open('ScrollDownComplete2.txt', 'a', encoding="utf-8")
        file.write(text)
        file.close()
        print('Text written to file: ' + str(os.path.basename(file.name)))
        end_time = time.time() - start_time
        print("Time: " + str(end_time))


def deEmojify(text):
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r'',text)


main()
