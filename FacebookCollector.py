#! python3
# FacebookCollector.py - Copies all Facebook posts from a page into a document.


from selenium import webdriver
import time
import re
import pyperclip
from selenium.webdriver.common.keys import Keys


def main():
    copying = True
    scroll_num = 4
    chunk_counter = 1
    PATH = "C:\Program Files (x86)\chromedriver.exe"
    driver = webdriver.Chrome(PATH)
    html_elem = open_page(driver)
    while copying:
        text = copy_posts(scroll_num, html_elem, driver)
        text_list = remove_extra_text(text)
        write_to_file(text_list, chunk_counter)
        copying = check_end(text)
        chunk_counter += 1
        scroll_num = 10


# Function to open the Facebook page in Google Chrome.
def open_page(driver):
    # Link to the tweets to copy.
    driver.get('https://www.facebook.com/pg/RepMcKinley/posts/?ref=page_internal')
    html_elem = driver.find_element_by_tag_name("body")
    return html_elem


def copy_posts(scroll_num, html_elem, driver):
    for i in range(scroll_num):
        html_elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.2)
    body = driver.find_element_by_css_selector('body')
    time.sleep(.5)
    body.send_keys(Keys.CONTROL + 'a')
    body.send_keys(Keys.CONTROL + 'c')
    text = str(pyperclip.paste())
    return text


def remove_extra_text(text):
    text = deEmojify(text)
    lines = text.split('\n')
    #lines = set(lines)
    text_list = []
    delete_lines = True
    delete_comments = False
    for line in lines:
        if line == 'Facebook © 2020\r':
            delete_lines = False
        if 'Comments' in line or 'Comment' in line:
            delete_comments = True
        if delete_comments is True and line == '\r':
            delete_comments = False
        if delete_lines is False and delete_comments is False:
            text_list.append(line)
    return text_list


# This function is taken from a thread on StackOverflow.
# Function used for removing emojis from the tweets, so Python is able to manipulate the text.
def deEmojify(text):
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r'',text)


def write_to_file(text_list, chunk_counter):
    file = open('McKinleyFacebookPostsFullTakeTwo.txt', 'a', encoding="utf-8")
    for i in text_list:
        file.write(i)
    file.close()
    print("Posts have been added to the document -- Chunk " + str(chunk_counter))


# Function to check if the loop has reached the end of the Twitter feed.
def check_end(text):
    copying = True
    # Date of the last tweet you want it to copy. The program will stop when it sees this date.
    if "January 19, 2011" in text:
        copying = False
    return copying


main()
