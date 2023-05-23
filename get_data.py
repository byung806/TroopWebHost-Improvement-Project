import requests
from bs4 import BeautifulSoup
import numpy as np


def log_in(session: requests.Session):
    with open('login.txt', 'r') as f:
        username, password = f.read().split('\n')[:2]

    payload = {
        'menuopenflag': 'N',
        'Selected_Action': 'login',
        'Menu_Item_ID': 49792,
        'Form_ID': 7323,
        'Pass': 1,
        'Stack': 1,
        'ChildRowID': 0,
        'Current_URL': 'https://www.troopwebhost.org/formCustom.aspx?Menu_Item_ID=49792&Custom_Form_ID=1',
        'User_Login': username,
        'User_Password': password,
        'Language_ID': 1,
        'Page_Layout': 1,
        'Report_option': 2,
        'Custom_Form_ID': 1,
        'FirstControl': 'User_Login',
    }

    LOGIN_URL = 'https://www.troopwebhost.org/formCustom.aspx'

    p = session.post(LOGIN_URL, data=payload)
    assert('Log Off' in p.text)


def get_html_page(session, url):
    response = session.get(url)
    return response.text


ADULT_TRAINING_URL = 'https://www.troopwebhost.org/FormList.aspx?Menu_Item_ID=45888&Stack=0'
SEND_EMAIL_URL = 'https://www.troopwebhost.org/FormDetail.aspx?Menu_Item_ID=45961&Stack=1'

with requests.Session() as session:
    session.cookies.set('Application_ID', '1338')
    log_in(session)

    session.cookies.set('RowsPerPage', 'ALL')

    adult_trainings_page = get_html_page(session, ADULT_TRAINING_URL)
    send_email_page = get_html_page(session, SEND_EMAIL_URL)

    with open('adult_trainings.html', 'w') as f:
        f.write(adult_trainings_page)
    with open('send_email.html', 'w') as f:
        f.write(send_email_page)


columns = {
    'Adult': 0,
    'BSA ID': 1,
    'Leadership': 2,
    'Training': 3,
    'Completed': 4,
    'Comment': 5,
    'Expires': 6,
    'Certificate': 7
}



soup = BeautifulSoup(adult_trainings_page, 'html.parser').tbody
for entry in soup.findAll('table'):
    row = np.empty(8, dtype=object)
    for tr in entry.findAll('tr', id=True):
        column_td = tr.find('td', class_='mobile-grid-caption')
        column = columns[column_td.text.strip()]  # could cause error if not in columns, or all_tds is empty

        data_td = tr.find('td', class_='mobile-grid-data')
        entry_item = data_td.text.strip()
        if entry_item == 'Certificate Document':
            entry_item = data_td.a['href']

        row[column] = entry_item
    print(row)
