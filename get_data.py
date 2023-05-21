import requests


def log_in(session: requests.Session):
    with open('login.txt', 'r') as f:
        username, password = f.read().split('\n')

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
    