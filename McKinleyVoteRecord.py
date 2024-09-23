#! python3
# McKinleyVoteRecord.py - Finds the voting record of Rep. McKinley and adds the data to a spreadsheet.
# Notes: There are 280 pages of votes on his website.


import bs4
import requests
import ezsheets


# Creates a Bill as an object. This will be able to store all of the bills collected.
class Bill:
    date = ''
    hr_number = ''
    vote = ''
    bill_name = ''
    subject = ''
    passed = ''
    source = ''

    def __init__(self, html, old_format):
        self.html = html
        self.old_format = old_format

    def get_date(self):
        time_elems = self.html.find_all('time')
        for i in time_elems:
            self.date = i.get('title')

    def get_hr_number(self):
        col2 = self.html.select('.col2')
        for i in col2:
            text = i.text.strip()
            self.hr_number = text

    def get_vote(self):
        col4 = self.html.select('.col4')
        for elem in col4:
            text = elem.text.strip()
            self.vote = text

    def get_name(self):
        if self.old_format is True:
            congress_num = find_congress_num(self)
            bill_num = self.hr_number.split(' ')[-1]
            congress_gov_link = 'https://www.congress.gov/bill/' + congress_num + 'th-congress/house-bill/' + bill_num
            congress_html = requests.get(congress_gov_link)
            link_works = True
            try:
                congress_html.raise_for_status()
            except Exception as exc:
                print('Error: %s' % exc)
                link_works = False
            if link_works is True:
                congress_soup = bs4.BeautifulSoup(congress_html.text, 'html.parser')
                name_elems = congress_soup.select('.legDetail')
                name1 = ''
                for name in name_elems:
                    name1 = name.text
                name1 = name1[:-26]
                name_list = name1.split(' ')
                name_list = name_list[2:]
                for i in name_list:
                    self.bill_name += i + ' '
        else:
            col5 = self.html.select('.col5')
            for i in col5:
                text = i.text.strip()
                self.bill_name = text

    def get_subject(self):
        link = ''
        if self.old_format is True:
            congress_num = find_congress_num(self)
            bill_num = self.hr_number.split(' ')[-1]
            congress_gov_link = 'https://www.congress.gov/bill/' + congress_num + 'th-congress/house-bill/' + bill_num
            self.source = congress_gov_link
            congress_html = requests.get(congress_gov_link)
            link_works = True
            try:
                congress_html.raise_for_status()
            except Exception as exc:
                print('Error: %s' % exc)
                link_works = False
            if link_works is True:
                link = congress_gov_link
        else:
            # Get link to congress.gov page for the bill.
            col2 = self.html.select('.col2')
            link = ''
            a_elems = []
            for i in col2:
                a_elems.append(i.find_all('a'))
            for a in a_elems:
                for i in a:
                    link = i.get('href')
                    self.source = link
            # Find subject on congress.gov page for the bill.
        congress_html = requests.get(link)
        congress_html.raise_for_status()
        congress_soup = bs4.BeautifulSoup(congress_html.text, 'html.parser')
        plain_class = congress_soup.select('.plain')
        subject_text = ''
        for i in plain_class:
            subject_text = i.text.strip()
        text_list = subject_text.split('\n')
        self.subject = text_list[0]
        return congress_soup

    def get_if_passed(self, congress_soup):
        ol_elems = congress_soup.find_all('ol')
        selected_list = []
        for elem in ol_elems:
            selected_list.append(elem.select('.selected'))
        text = ''
        for i in selected_list:
            for t in i:
                text = t.text.strip()
        text_list = text.split('\n')
        text2 = text_list[0]
        if text2 == 'IntroducedArray':
            self.passed = 'No'
        else:
            self.passed = 'Yes'


def main():
    final_bill_list = []
    for i in range(281):
        vote_elem_lists = get_vote_elems(i)
        bill_list = get_vote_info(vote_elem_lists)
        for bill in bill_list:
            final_bill_list.append(bill)
        print('Page %s done' % str(i))
    subject_list = find_subjects(final_bill_list)
    add_to_sheets(final_bill_list, subject_list)
    print('Done')


# Gets the html element for each bill, and returns them in a list.
def get_vote_elems(page_index):
    #page_url = 'https://mckinley.house.gov/voterecord/'
    page_url = 'https://mckinley.house.gov/voterecord/?Page=' + str(page_index)
    page_html = requests.get(page_url)
    page_html.raise_for_status()
    page_soup = bs4.BeautifulSoup(page_html.text, 'html.parser')
    tbody_elems = page_soup.find_all('tbody')
    vote_elems = []
    vote_elems_old_format = []
    for i in tbody_elems:
        all_votes = i.find_all('tr')
        for elem in all_votes:
            col3 = elem.select('.col3')
            for t in col3:
                if t.text.strip() == 'On Passage of the Bill':
                    vote_elems.append(elem)
                if t.text.strip() == 'On Passage':
                    vote_elems_old_format.append(elem)
    vote_elem_lists = [vote_elems, vote_elems_old_format]
    return vote_elem_lists


# Uses the Bill class to get information on each bill, and store it in the Bill objects.
def get_vote_info(vote_elem_lists):
    bill_list = []
    new_vote_elems = vote_elem_lists[0]
    old_vote_elems = vote_elem_lists[1]
    for vote_html in new_vote_elems:
        bill = Bill(vote_html, False)
        bill.get_date()
        bill.get_hr_number()
        bill.get_vote()
        bill.get_name()
        congress_soup = bill.get_subject()
        bill.get_if_passed(congress_soup)
        bill_list.append(bill)
    for vote_html in old_vote_elems:
        bill = Bill(vote_html, True)
        bill.get_date()
        bill.get_hr_number()
        bill.get_vote()
        bill.get_name()
        congress_soup = bill.get_subject()
        bill.get_if_passed(congress_soup)
        bill_list.append(bill)
    return bill_list


# Finds all of the different subjects of the bills.
def find_subjects(bill_list):
    subject_list = []
    for bill in bill_list:
        if bill.subject not in subject_list:
            subject_list.append(bill.subject)
    return subject_list


# Finds the number of congress based on the year the bill was written, in order to be able to search for the bill
# on congress.gov.
def find_congress_num(bill):
    year = bill.date[-4:]
    congress_num = ''
    if year == '2011' or year == '2012':
        congress_num = '112'
    if year == '2013' or year == '2014':
        congress_num = '113'
    if year == '2015' or year == '2016':
        congress_num = '114'
    if year == '2017' or year == '2018':
        congress_num = '115'
    if year == '2019' or year == '2020':
        congress_num = '116'
    return congress_num


# Add the voting record to a Google Spreadsheet.
def add_to_sheets(bill_list, subject_list):
    spread = ezsheets.Spreadsheet('https://docs.google.com/spreadsheets/d/1F_ewPduuWAINqofQmdesHN-jEo5GvIhkE8wWxpDNS98/edit#gid=0')
    for subject in subject_list:
        spread.createSheet(subject)
    spread[0].delete()
    for title in spread.sheetTitles:
        sheet = spread[title]
        sheet.updateRow(1, ['Bill Name', 'Bill #', 'Did the bill pass?', "McKinley's Vote", 'Source'])
    row_num_list = []
    for i in range(len(spread.sheetTitles)):
        row_num_list.append(2)
    for bill in bill_list:
        sheet = spread[subject_list.index(bill.subject)]
        sheet.updateRow(row_num_list[subject_list.index(bill.subject)], [bill.bill_name, bill.hr_number, bill.passed, bill.vote, bill.source])
        row_num_list[subject_list.index(bill.subject)] += 1


main()
