import pytest
import environ
import pickle
from selenium import webdriver

env = environ.Env()
environ.Env.read_env()


@pytest.fixture(scope='session', autouse=True)
def login(request):
    SUPPORTED_DRIVERS = {
        "BrowserStack": webdriver.Remote,
        "CrossBrowserTesting": webdriver.Remote,
        "Chrome": webdriver.Chrome,
        "Edge": webdriver.Edge,
        "Firefox": webdriver.Firefox,
        "IE": webdriver.Ie,
        "Remote": webdriver.Remote,
        "Safari": webdriver.Safari,
        "SauceLabs": webdriver.Remote,
        "TestingBot": webdriver.Remote,
    }

    driver = request.config.getoption("driver")
    browser = SUPPORTED_DRIVERS[driver]()

    browser.get(f'{env("BASE_URL")}/login')

    field_email = browser.find_element_by_id("email")
    field_email.click()
    field_email.clear()
    field_email.send_keys(env('USER_EMAIL'))

    field_pass = browser.find_element_by_id("pass")
    field_pass.click()
    field_pass.clear()
    field_pass.send_keys(env('USER_PASSWORD'))

    btn_submit = browser.find_element_by_xpath(
        "//button[@type='submit']")
    btn_submit.click()

    # Save cookies of the browser after the login
    with open('cookies.txt', 'wb') as cookies:
        pickle.dump(browser.get_cookies(), cookies)


@pytest.fixture()
def registered_user(selenium):
    selenium.get(f'{env("BASE_URL")}')
    cookies = pickle.load(open("cookies.txt", "rb"))
    for cookie in cookies:
        print(cookie)
        selenium.add_cookie(cookie)
