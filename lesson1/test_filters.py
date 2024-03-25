import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

# Фикстура для настройки драйвера
@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Chrome() # Указать путь к WebDriver, если он не в PATH
    driver.get("https://www.saucedemo.com/")
    login(driver)
    yield driver
    driver.quit()

def login(driver):
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

def get_product_names(driver):
    return [item.text for item in driver.find_elements(By.CLASS_NAME, "inventory_item_name")]

def get_product_prices(driver):
    return [float(price.text.replace('$','')) for price in driver.find_elements(By.CLASS_NAME, "inventory_item_price")]

@pytest.mark.parametrize('filter_type, expected_order', [
    ('az', 'A to Z'),
    ('za', 'Z to A'),
    ('lohi', 'Low to High'),
    ('hilo', 'High to Low'),
])
def test_product_filter(driver, filter_type, expected_order):
    select = Select(driver.find_element(By.CLASS_NAME, 'product_sort_container'))
    select.select_by_value(filter_type)
    if expected_order in ['A to Z', 'Z to A']:
        items = get_product_names(driver)
        sorted_items = sorted(items, reverse=expected_order=='Z to A')
        assert items == sorted_items, f"Items were not sorted {expected_order}"
    else:
        prices = get_product_prices(driver)
        sorted_prices = sorted(prices, reverse=expected_order=='High to Low')
        assert prices == sorted_prices, f"Prices were not sorted {expected_order}"
