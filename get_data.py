import aiohttp
import asyncio
from bs4 import BeautifulSoup
import numpy as np


# Log in using a POST request in a session
async def log_in(session, username, password):
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

    async with session.post(LOGIN_URL, data=payload) as response:
        assert response.status == 200
        # Returns whether or not login was successful
        return await 'Log Off' in response.text()


# Use GET request to get HTML at an URL (in a logged in session)
async def get_html_page(session, url):
    async with session.get(url) as response:
        assert response.status == 200
        return await response.text()


async def get_logged_in_session(username, password):
    # Application ID of Troop 1094 Darnestown is 1338
    cookies = {'RowsPerPage': 'ALL', 'Application_ID': '1338'}
    async with aiohttp.ClientSession(cookies=cookies) as session:
        login_successful = await log_in(session, username, password)
        # Returns logged in session or None if login failed
        return session if login_successful else None
        

# Main function to scrape all the data and format it
async def get_data(logged_in_session):
    ADULT_TRAINING_URL = 'https://www.troopwebhost.org/FormList.aspx?Menu_Item_ID=45888&Stack=0'
    SEND_EMAIL_URL = 'https://www.troopwebhost.org/FormDetail.aspx?Menu_Item_ID=45961&Stack=1'

    adult_trainings_page = await get_html_page(logged_in_session, ADULT_TRAINING_URL)
    send_email_page = await get_html_page(logged_in_session, SEND_EMAIL_URL)

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
    

# For testing
if __name__ == '__main__':
    get_data(get_logged_in_session('sdraisen', 'My3scouts'))