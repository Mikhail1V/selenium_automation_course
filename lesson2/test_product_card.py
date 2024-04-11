import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Локаторы
USER_NAME_INPUT = (By.ID, "user-name")
PASSWORD_INPUT = (By.ID, "password")
LOGIN_BUTTON = (By.ID, "login-button")
INVENTORY_ITEM_IMG = (By.CLASS_NAME, "inventory_item_img")
INVENTORY_ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
ITEM_PAGE_SUFFIX = "inventory-item.html"

# Данные для входа
USERNAME = "standard_user"
PASSWORD = "secret_sauce"

# Фикстура для подготовки драйвера
@pytest.fixture(scope="function")
def driver():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get("https://www.saucedemo.com/")
    yield driver
    driver.quit()

# Функция логина
def perform_login(driver):
    driver.find_element(*USER_NAME_INPUT).send_keys(USERNAME)
    driver.find_element(*PASSWORD_INPUT).send_keys(PASSWORD)
    driver.find_element(*LOGIN_BUTTON).click()

# Фикстура для входа в систему
@pytest.fixture(scope="function")
def login(driver):
    perform_login(driver)

# Тесты
def test_transition_by_clicking_image(driver, login):
    driver.find_elements(*INVENTORY_ITEM_IMG)[0].click()
    assert ITEM_PAGE_SUFFIX in driver.current_url, "Did not transition to product card after clicking image"

def test_transition_by_clicking_title(driver, login):
    driver.find_elements(*INVENTORY_ITEM_NAME)[0].click()
    assert ITEM_PAGE_SUFFIX in driver.current_url, "Did not transition to product card after clicking title"