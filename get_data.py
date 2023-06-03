import requests
from bs4 import BeautifulSoup
import numpy as np


# Log in using a POST request in a session
def log_in(session: requests.Session):
    #TODO: get credentials from login
    with open('login.txt', 'r') as f:
        username, password = f.read().split('\n')[:2]

    payload = {
        'Selected_Action': 'login',
        'Menu_Item_ID': 49792,
        'Form_ID': 7323,
        'Pass': 1,
        'Current_URL': 'https://www.troopwebhost.org/formCustom.aspx',
        'User_Login': username,
        'User_Password': password,
    }

    LOGIN_URL = 'https://www.troopwebhost.org/formCustom.aspx'

    p = session.post(LOGIN_URL, data=payload)
    # Make sure login was successful
    return 'Log Off' in p.text


# Use GET request to get HTML at an URL (in a logged in session)
def get_html_page(session, url):
    response = session.get(url)
    return response.text


# Main function to scrape all the data and format it
def get_data():
    ADULT_TRAINING_URL = 'https://www.troopwebhost.org/FormList.aspx?Menu_Item_ID=45888&Stack=0'
    SEND_EMAIL_URL = 'https://www.troopwebhost.org/FormDetail.aspx?Menu_Item_ID=45961&Stack=1'
    
    with requests.Session() as session:
        # Application ID of Troop 1094 Darnestown
        session.cookies.set('Application_ID', '1338')
        login_successful = log_in(session)
        if not login_successful:
            return False

        # Cookie to request all data on one page
        session.cookies.set('RowsPerPage', 'ALL')
    
        adult_trainings_page = get_html_page(session, ADULT_TRAINING_URL)
        send_email_page = get_html_page(session, SEND_EMAIL_URL)

    # Columns of the data with names, for use when parsing
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

    # Object to help parse HTML (.tbody finds first <tbody> element)
    soup = BeautifulSoup(adult_trainings_page, 'html.parser').tbody

    # Temporary array to store extracted rows from the HTML
    rows = []
    # soup.findAll finds all <table> tags in the HTML
    for entry in soup.findAll('table'):
        # Loop through each data entry
        row = np.empty(8, dtype=object)
        # For each <tr> tag 
        for tr in entry.findAll('tr', id=True):
            column_td = tr.find('td', class_='mobile-grid-caption')
            # Each column of text is stored inside a <td> tag in this particular table in the HTML
            column = columns[column_td.text.strip()]  # could cause error if not in columns
    
            data_td = tr.find('td', class_='mobile-grid-data')
            entry_item = data_td.text.strip()
            if entry_item == 'Certificate Document':
                entry_item = data_td.a['href']
    
            row[column] = entry_item
        rows.append(row)

    # Assemble contents of rows array into 2d array with all the data
    adult_training_data = np.vstack(rows)
    # TODO: do the same thing with send_email_page variable using BeautifulSoup
    

if __name__ == '__main__':
    get_data()