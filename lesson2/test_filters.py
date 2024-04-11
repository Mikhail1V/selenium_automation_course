import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager

# Локаторы
USERNAME_INPUT = (By.ID, "user-name")
PASSWORD_INPUT = (By.ID, "password")
LOGIN_BUTTON = (By.ID, "login-button")
PRODUCT_NAME = (By.CLASS_NAME, "inventory_item_name")
PRODUCT_PRICE = (By.CLASS_NAME, "inventory_item_price")
PRODUCT_SORT_CONTAINER = (By.CLASS_NAME, 'product_sort_container')

# Тестовые данные
VALID_USERNAME = "standard_user"
VALID_PASSWORD = "secret_sauce"

# Фикстура для настройки и закрытия веб-драйвера
@pytest.fixture(scope="function")
def driver():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get("https://www.saucedemo.com/")
    yield driver
    driver.quit()

# Фикстура для авторизации
@pytest.fixture(scope="function")
def login(driver):
    driver.find_element(*USERNAME_INPUT).send_keys(VALID_USERNAME)
    driver.find_element(*PASSWORD_INPUT).send_keys(VALID_PASSWORD)
    driver.find_element(*LOGIN_BUTTON).click()

# Вспомогательные функции для получения информации о товарах
def get_product_names(driver):
    return [item.text for item in driver.find_elements(*PRODUCT_NAME)]

def get_product_prices(driver):
    prices = driver.find_elements(*PRODUCT_PRICE)
    return [float(price.text.replace('$', '')) for price in prices]

# Тесты
@pytest.mark.parametrize('filter_type, expected_order', [
    ('az', 'A to Z'),
    ('za', 'Z to A'),
    ('lohi', 'Low to High'),
    ('hilo', 'High to Low'),
])
def test_product_filter(driver, login, filter_type, expected_order):
    select = Select(driver.find_element(*PRODUCT_SORT_CONTAINER))
    select.select_by_value(filter_type)

    if expected_order in ['A to Z', 'Z to A']:
        items = get_product_names(driver)
        sorted_items = sorted(items, reverse=expected_order=='Z to A')
        assert items == sorted_items, f"Items were not sorted {expected_order}"
    elif expected_order in ['Low to High', 'High to Low']:
        prices = get_product_prices(driver)
        sorted_prices = sorted(prices, reverse=expected_order=='High to Low')
        assert prices == sorted_prices, f"Prices were not sorted {expected_order}"