import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

# Фикстура для настройки драйвера и входа в приложение
@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Chrome()  # или путь к вашему WebDriver
    driver.get("https://www.saucedemo.com/")
    login(driver)
    yield driver
    driver.quit()

def login(driver):
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

def test_add_to_cart_from_catalog(driver):
    driver.find_element(By.CLASS_NAME, "btn_inventory").click()
    cart_badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text
    assert cart_badge == "1", "Item was not added to the cart"

def test_remove_from_cart(driver):
    test_add_to_cart_from_catalog(driver)
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    driver.find_element(By.CLASS_NAME, "cart_button").click()
    cart_items = driver.find_elements(By.CLASS_NAME, "cart_item")
    assert len(cart_items) == 0, "Item was not removed from the cart"

def test_add_to_cart_from_item_page(driver):
    driver.find_element(By.CLASS_NAME, "inventory_item_name").click()
    driver.find_element(By.CLASS_NAME, "btn_inventory").click()
    cart_badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text
    assert cart_badge == "1", "Item was not added to the cart from the item page"

def test_remove_from_cart_item_page(driver):
    test_add_to_cart_from_item_page(driver)
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    driver.find_element(By.CLASS_NAME, "cart_button").click()
    cart_items = driver.find_elements(By.CLASS_NAME, "cart_item")
    assert len(cart_items) == 0, "Item was not removed from the cart from the item page"