#! python3
# NewsWebsiteScraper.py - Scrapes different websites for news articles on a certain topic and saves the articles
# into a text file.

import bs4
import requests
import webbrowser
import re


def main():
    # Opens a text file to write the articles to.
    file = open('C:/Users/kerry/Documents/NatalieClineDocuments/McKinleyNewsArticleFiles/WVNewsMcKinleyArticlesText.txt', 'a', encoding='utf-8')
    # Collects the articles from the websites.
    wvnews(file)
    # Closes the file.
    file.close()
    print('\n\n Done')


# Searches articles on wboy.com
def wboy(file):
    chrome = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
    final_text_list2 = []
    final_text_list3 = []
    # Get search term from user.
    term = input("Search term: ")
    s = ''
    for i in term.split(" "):
        s += i + '+'
    s = s[:-1]
    # Get HTML text from the website.
    search_page_url = 'https://www.wboy.com/?s=%s&submit=Search' % s
    first_page_done = False
    index = 0
    # There are 12 full pages of articles.
    for loop in range(12):
        if first_page_done is True:
            res = requests.get(search_page_url)
            res.raise_for_status()
            soup = bs4.BeautifulSoup(res.text, 'html.parser')
            next_page_elem = soup.select('.nav-previous')
            for i in next_page_elem[0]:
                search_page_url = i.get('href')
        res = requests.get(search_page_url)
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text, 'html.parser')
        searchpage_soup = soup.find_all('article')
        article_links_elems = []
        for i in searchpage_soup:
            a_elem = i.find_all('a')
            article_links_elems.append(a_elem)
        # Remove unwanted article HTML elements.
        for i in range(14):
            article_links_elems.remove(article_links_elems[0])
        for i in range(10):
            article_links_elems.remove(article_links_elems[10])
        # Get article links.
        article_links = []
        for elem in article_links_elems:
            for i in elem:
                article_links.append(i.get('href'))
        # Get the text from each article
        for article_link in article_links:
            index += 1
            file.write('\n')
            file.write('\n')
            print('Article #%s' % str(index))
            file.write('Article #%s' % str(index))
            article_link_html = requests.get(article_link)
            article_link_html.raise_for_status()
            article_soup = bs4.BeautifulSoup(article_link_html.text, 'html.parser')
            h1_soup = article_soup.find_all('h1')
            for title in h1_soup:
                print(title.text)
                file.write(title.text)
                file.write('\n')
                file.write('\n')
            text_soup = article_soup.find_all('div')
            p_list = []
            for elem in text_soup:
                p = elem.find_all('p')
                for text in p:
                    p_list.append(text.text)
            final_text_list = []
            for i in p_list:
                if i not in final_text_list:
                    final_text_list.append(i)
            final_text_list2 = []
            append = True
            for i in final_text_list:
                if i.split(" ")[0] == 'Copyright':
                    append = False
                if append is True:
                    final_text_list2.append(i)
            for i in final_text_list2:
                file.write(i)
                #file.write('\n')
                #file.write('\n')
        first_page_done = True


def wboy_page13(file):
    search_page_url = 'https://www.wboy.com/page/13/?s=David+McKinley&submit=Search'
    res = requests.get(search_page_url)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    searchpage_soup = soup.find_all('article')
    article_links_elems = []
    for i in searchpage_soup:
        a_elem = i.find_all('a')
        article_links_elems.append(a_elem)
    index = -1
    appending = False
    article_links_elems2 = []
    for i in article_links_elems:
        index += 1
        if index == 14:
            appending = True
        if index == 20:
            appending = False
        if appending is True:
            article_links_elems2.append(i)
    article_links = []
    for elem in article_links_elems2:
        for i in elem:
            article_links.append(i.get('href'))
    index = 120
    for link in article_links:
        index += 1
        file.write('\n \n')
        file.write('Article #%s' % str(index))
        article_html = requests.get(link)
        article_html.raise_for_status()
        article_soup = bs4.BeautifulSoup(article_html.text, 'html.parser')
        h1_soup = article_soup.find_all('h1')
        for title in h1_soup:
            print(title.text)
            file.write(title.text)
            file.write('\n')
            file.write('\n')
        text_soup = article_soup.find_all('div')
        p_list = []
        for elem in text_soup:
            p = elem.find_all('p')
            for text in p:
                p_list.append(text.text)
        final_text_list = []
        for i in p_list:
            if i not in final_text_list:
                final_text_list.append(i)
        final_text_list2 = []
        append = True
        for i in final_text_list:
            if i.split(" ")[0] == 'Copyright':
                append = False
            if append is True:
                final_text_list2.append(i)
        for i in final_text_list2:
            file.write(i)


# Searches articles on theintermountain.com and adds them to a text file.
def theintermountain(file):
    # Note: There are only 11 pages of articles for David McKinley, but there are 100 pages listed.
    article_num = 0
    for index in range(1, 12):
        search_page_url = 'https://www.theintermountain.com/search/David%20McKinley/page/' + str(index) + '/'
        res = requests.get(search_page_url)
        res.raise_for_status()
        searchpage_soup = bs4.BeautifulSoup(res.text, 'html.parser')
        article_link_soup = searchpage_soup.find_all('article')
        article_link_elems = []
        for i in article_link_soup:
            article_link_elems.append(i.find_all('a'))
        article_links = []
        titles = []
        for elem in article_link_elems:
            for i in elem:
                article_links.append(i.get('href'))
                h1 = i.find_all('h1')
                for h in h1:
                    titles.append(h.text)
        title_index = -1
        for article in article_links:
            title_index += 1
            article_num += 1
            print('\nArticle #%s' % str(article_num) + '\n')
            article_working = True
            article_html = requests.get(article)
            try:
                article_html.raise_for_status()
            except Exception as exc:
                print('There was a problem: %s' % exc)
                article_working = False
            if article_working is True:
                file.write('\nArticle #%s' % str(article_num) + '\n')
                file.write('\n')
                try:
                    print('Title: %s' % titles[title_index] + '\n')
                    file.write('Title: %s' % titles[title_index] + '\n')
                    file.write('\n')
                except IndexError:
                    print('Title not found.\n')
                    file.write('Title not found.\n')
                    file.write('\n')
                article_soup = bs4.BeautifulSoup(article_html.text, 'html.parser')
                sections = article_soup.select('#article_content')
                for i in sections:
                    p_elem = i.find_all('p')
                    for p in p_elem:
                        file.write(p.text)
            print('\n')
            file.write('\n')


# Searches the news website News and Sentinel and copies articles to a text file.
def newsandsentinel(file):
    article_num = 0
    for index in range(1, 30):
        search_page_url = 'https://www.newsandsentinel.com/search/David+McKinley/page/' + str(index) + '/'
        res = requests.get(search_page_url)
        res.raise_for_status()
        searchpage_soup = bs4.BeautifulSoup(res.text, 'html.parser')
        article_link_soup = searchpage_soup.find_all('article')
        article_link_elems = []
        for i in article_link_soup:
            article_link_elems.append(i.find_all('a'))
        article_links = []
        titles = []
        for elem in article_link_elems:
            for i in elem:
                article_links.append(i.get('href'))
                h1 = i.find_all('h1')
                for h in h1:
                    titles.append(h.text)
        title_index = -1
        for article in article_links:
            title_index += 1
            article_num += 1
            print('\nArticle #%s' % str(article_num) + '\n')
            article_working = True
            article_html = requests.get(article)
            try:
                article_html.raise_for_status()
            except Exception as exc:
                print('There was a problem: %s' % exc)
                article_working = False
            if article_working is True:
                file.write('\nArticle #%s' % str(article_num) + '\n')
                file.write('\n')
                try:
                    print('Title: %s' % titles[title_index] + '\n')
                    file.write('Title: %s' % titles[title_index] + '\n')
                    file.write('\n')
                except IndexError:
                    print('Title not found.\n')
                    file.write('Title not found.\n')
                    file.write('\n')
                article_soup = bs4.BeautifulSoup(article_html.text, 'html.parser')
                sections = article_soup.select('#article_content')
                for i in sections:
                    p_elem = i.find_all('p')
                    for p in p_elem:
                        file.write(p.text)
                        #print(p.text)
            print('\n')
            file.write('\n')


# Searches articles from the news website wvmetronews.com and adds the articles to a text file.
def wvmetronews(file):
    article_num = 0
    year_list = ['', '+2020', '+2019', '+2018', '+2017', '+2016', '+2015', '+2014', '+2013', '+2012', '+2011']
    #year_list = ['']
    for year in year_list:
        search_page_url = 'https://wvmetronews.com/?s=David+McKinley' + year
        res = requests.get(search_page_url)
        res.raise_for_status()
        searchpage_soup = bs4.BeautifulSoup(res.text, 'html.parser')
        article_elem_soup = searchpage_soup.find_all('article')
        h2_elems = []
        for i in article_elem_soup:
            h2_elems.append(i.find_all('h2'))
        article_link_elems = []
        for elem in h2_elems:
            for i in elem:
                article_link_elems.append(i.find_all('a'))
        article_links = []
        titles = []
        for elem in article_link_elems:
            for i in elem:
                article_links.append(i.get('href'))
                titles.append(i.text)
        titles_index = -1
        for article in article_links:
            titles_index += 1
            article_num += 1
            print('\n')
            file.write('\n')
            print('Article #%s' % str(article_num) + '\n')
            article_html = requests.get(article)
            article_working = True
            try:
                article_html.raise_for_status()
            except Exception as exc:
                print('There was an error: %s' % exc)
                article_working = False
            if article_working is True:
                file.write('\n')
                file.write('Article #%s' % str(article_num))
                file.write('\n')
                try:
                    print('Title: %s' % titles[titles_index] + '\n')
                    file.write('Title: %s' % titles[titles_index])
                    file.write('\n')
                except Exception as exc:
                    print('Title not found. Error: %s' % exc)
                    file.write('Title not found')
                    file.write('\n')
                article_html_soup = bs4.BeautifulSoup(article_html.text, 'html.parser')
                article_elem_soup = article_html_soup.find_all('article')
                for i in article_elem_soup:
                    p_elem = i.find_all('p')
                    for p in p_elem:
                        #print(p.text)
                        file.write(p.text)
        print('\n')
        file.write('\n')


# Searches for articles on wvnews.com
def wvnews(file):
    article_num = 0
    # Needs to iterate 42 times to get through all search pages.
    for num in range(42):
        search_page_url = 'https://www.wvnews.com/search/?l=25&sort=relevance&f=html&t=article%2Cvideo%2Cyoutube%2Ccollection&app%5B0%5D=editorial&nsa=eedition&q=David+McKinley&o=' + str(num*25)
        searchpage_html = requests.get(search_page_url)
        searchpage_html.raise_for_status()
        searchpage_soup = bs4.BeautifulSoup(searchpage_html.text, 'html.parser')
        div_elems = searchpage_soup.find_all('div')
        h3_list = []
        for elem in div_elems:
            h3_list.append(elem.find_all('h3'))
        a_elem_list = []
        for h3 in h3_list:
            for i in h3:
                a_elem_list.append(i.find_all('a'))
        article_links = []
        for a in a_elem_list:
            for i in a:
                link_base = i.get('href')
                link = 'https://wvnews.com' + link_base
                article_links.append(link)
        index_num = 0
        title_list = []
        title_in_url_list = []
        true_url_list = []
        for link in article_links:
            index_num += 1
            title_in_url = find_title_in_url(link)
            duplicate = False
            if title_in_url not in title_in_url_list:
                title_in_url_list.append(title_in_url)
            else:
                duplicate = True
            if duplicate is False:
                true_url_list.append(link)
                article_html = requests.get(link)
                article_html.raise_for_status()
                full_page_soup = bs4.BeautifulSoup(article_html.text, 'html.parser')
                article_div_elems = full_page_soup.find_all('div')
                h1_elems = []
                for elem in article_div_elems:
                    h1_elems.append(elem.find_all('h1'))
                span_elems = []
                for elem in h1_elems:
                    for i in elem:
                        #print('span')
                        span_elems.append(i.find_all('span'))
                for s in span_elems:
                    for z in s:
                        z = z.text.strip()
                        if z not in title_list:
                            title_list.append(z)
        title_index = -1
        for url in true_url_list:
            article_num += 1
            print('Article #%s' % str(article_num))
            file.write('Article #%s' % str(article_num))
            file.write('\n')
            title_index += 1
            try:
                print(title_list[title_index])
                file.write(title_list[title_index])
                file.write('\n')
            except IndexError:
                print('Title not found.')
                file.write('Title not found.')
                file.write('\n')
            #print(url)
            print('\n')
            article_html2 = requests.get(url)
            article_html2.raise_for_status()
            article_full_page_soup = bs4.BeautifulSoup(article_html2.text, 'html.parser')
            div_elems2 = article_full_page_soup.find_all('div')
            subscriber_class = []
            for elem in div_elems2:
                subscriber_class.append(elem.select('.subscriber-preview'))
                subscriber_class.append(elem.select('.subscriber-only'))
            p_elem_list = []
            for elem in subscriber_class:
                for i in elem:
                    p_elem_list.append(i.find_all('p'))
            text_list = []
            for i in p_elem_list:
                for p in i:
                    #print(p.text)
                    if p.text not in text_list:
                        text_list.append(p.text)
            for text in text_list:
                file.write(text)
            #print('\n\n\n')
            for i in range(3):
                file.write('\n')


def find_title_in_url(url):
    url_split = list(url)
    url_split.reverse()
    title_list = []
    append = False
    for letter in url_split:
        if letter == '/' and append is True:
            break
        if letter == '/':
            append = True
        if append is True:
            title_list.append(letter)
    title_list.reverse()
    title_in_url = ''
    for letter in title_list:
        title_in_url += letter
    return title_in_url


main()
