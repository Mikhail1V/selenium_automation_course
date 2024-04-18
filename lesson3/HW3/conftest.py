import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait


@pytest.fixture()
def driver():
    print(f'\nStart test')
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument('--start-maximized')
    browser = webdriver.Chrome(options=chrome_options)
    yield browser
    browser.quit()
    print("\nEnd test")


@pytest.fixture
def wait(driver):
    wait = WebDriverWait(driver, timeout=10)
    return wait


@pytest.fixture()
def browser():
    print(f'\nStart test')
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument('--start-maximized')
    browser = webdriver.Chrome(options=chrome_options)
    browser.implicitly_wait(10)
    yield browser
    browser.quit()
    print("\nEnd test")