import requests
from bs4 import BeautifulSoup
import numpy as np


# Log in using a POST request in a session
def log_in(session, username, password):
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
    # Returns whether or not login was successful
    return 'Log Off' in p.text


# Use GET request to get HTML at an URL (in a logged in session)
def get_html_page(session, url):
    response = session.get(url)
    return response.text


def get_logged_in_session(username, password):
    with requests.Session() as session:
        # Application ID of Troop 1094 Darnestown
        session.cookies.set('Application_ID', '1338')
        login_successful = log_in(session, username, password)
        # Returns logged in session or None if login failed
        return session if login_successful else None
        

# Main function to scrape all the data and format it
def get_data(logged_in_session):
    ADULT_TRAINING_URL = 'https://www.troopwebhost.org/FormList.aspx?Menu_Item_ID=45888&Stack=0'
    SEND_EMAIL_URL = 'https://www.troopwebhost.org/FormDetail.aspx?Menu_Item_ID=45961&Stack=1'

    print(logged_in_session)
    adult_trainings_page = get_html_page(logged_in_session, ADULT_TRAINING_URL)
    send_email_page = get_html_page(logged_in_session, SEND_EMAIL_URL)

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
    adult_training_data = []
    # soup.findAll finds all <table> tags in the HTML
    for entry in soup.findAll('table'):
        # Loop through each data entry
        row = ['' for _ in range(9)]
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
        adult_training_data.append(row)

    # Assemble contents of rows array into 2d array with all the data


    # Do the same thing with send_email_page variable using BeautifulSoup
    columns = {
        'Name': 0,
        'Adult': 1,
        'Patrol': 2,
        'Leadership': 3,
        'Rank': 4,
        'Email': 5,
        'SMS': 6,
    }

    email_data = {}
    soup = BeautifulSoup(send_email_page, 'html.parser')
    tbody = soup.findAll('tbody')[1]
    for tr in tbody.findAll('tr'):
        entries_td = tr.findAll('td')[1]
        labels = entries_td.findAll('span')
        values = entries_td.findAll('div')
        pairs = zip(labels, values)
        row = ['' for _ in range(6)]
        row.append(list())
        for (label, value) in pairs:
            label = label.text.strip()
            if label == 'Email':
                # Workaround since .text ignores <br> (line break) tags
                possible_emails = str(value).split('>')[1:]
                if '@' in possible_emails[1]:
                    value = [possible_emails[0][:-4].strip(), possible_emails[1][:-5].strip()]
                else:
                    value = [possible_emails[0][:-5].strip()]
            else:
                value = value.text.strip()
            column = columns[label]
            row[column] = value
        # If person is an adult
        if row[1] == 'Y':
            email_data[row[0]] = row[5]

    # Combine two sets of data into columns:
    # Name, Training, Expiry Date, Email
    adult_training_data = [[p[0], p[3], p[6], *email_data[p[0]]] for p in adult_training_data]
    return adult_training_data    


# For testing
if __name__ == '__main__':
    get_data()