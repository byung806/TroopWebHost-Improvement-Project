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

    login_url = 'https://www.troopwebhost.org/formCustom.aspx'

    p = session.post(login_url, data=payload)
    assert('Log Off' in p.text)


def get_adult_trainings_page(session):
    adult_trainings_url = 'https://www.troopwebhost.org/FormList.aspx?Menu_Item_ID=45888&Stack=0%27,%27'

    response = session.get(adult_trainings_url)
    return response.text


with requests.Session() as session:
    session.cookies.set('Application_ID', '1338')
    log_in(session)

    adult_trainings = get_adult_trainings_page(session)
