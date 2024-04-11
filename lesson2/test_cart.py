import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Локаторы
USERNAME_FIELD = (By.ID, "user-name")
PASSWORD_FIELD = (By.ID, "password")
LOGIN_BUTTON = (By.ID, "login-button")
ADD_TO_CART_BUTTONS = (By.CLASS_NAME, "btn_inventory")
CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
SHOPPING_CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
CART_ITEMS = (By.CLASS_NAME, "cart_item")
CART_REMOVE_BUTTONS = (By.CLASS_NAME, "cart_button")
INVENTORY_ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")

# Тестовые данные
VALID_USERNAME = "standard_user"
VALID_PASSWORD = "secret_sauce"


@pytest.fixture(scope="function")
def driver():
    # Setup
    service = Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=service)
    browser.implicitly_wait(10)  # Используйте неявные ожидания для элементов
    browser.get("https://www.saucedemo.com/")
    # Вход в приложение
    browser.find_element(*USERNAME_FIELD).send_keys(VALID_USERNAME)
    browser.find_element(*PASSWORD_FIELD).send_keys(VALID_PASSWORD)
    browser.find_element(*LOGIN_BUTTON).click()
    yield browser
    # Teardown
    browser.quit()


# Вспомогательные функции
def add_first_item_to_cart(driver):
    driver.find_elements(*ADD_TO_CART_BUTTONS)[0].click()


def remove_first_item_from_cart(driver):
    driver.find_elements(*CART_REMOVE_BUTTONS)[0].click()


# Тесты
def test_add_to_cart_from_catalog(driver):
    add_first_item_to_cart(driver)
    cart_badge_text = driver.find_element(*CART_BADGE).text
    assert cart_badge_text == "1", "Item was not added to the cart"


def test_remove_from_cart(driver):
    add_first_item_to_cart(driver)
    driver.find_element(*SHOPPING_CART_LINK).click()
    remove_first_item_from_cart(driver)
    cart_items = driver.find_elements(*CART_ITEMS)
    assert len(cart_items) == 0, "Item was not removed from the cart"


def test_add_to_cart_from_item_page(driver):
    driver.find_elements(*INVENTORY_ITEM_NAMES)[0].click()
    add_first_item_to_cart(driver)
    cart_badge_text = driver.find_element(*CART_BADGE).text
    assert cart_badge_text == "1", "Item was not added to the cart from the item page"


def test_remove_from_cart_item_page(driver):
    driver.find_elements(*INVENTORY_ITEM_NAMES)[0].click()
    add_first_item_to_cart(driver)
    driver.find_element(*SHOPPING_CART_LINK).click()
    remove_first_item_from_cart(driver)
    cart_items = driver.find_elements(*CART_ITEMS)
    assert len(cart_items) == 0, "Item was not removed from the cart from the item page"
