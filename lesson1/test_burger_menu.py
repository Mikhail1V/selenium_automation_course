import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Chrome()  # Укажите путь к своему WebDriver, если он не в PATH
    driver.get("https://www.saucedemo.com/")
    login(driver)
    yield driver
    driver.quit()

def login(driver):
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

def open_burger_menu(driver):
    driver.find_element(By.ID, "react-burger-menu-btn").click()

def test_logout(driver):
    open_burger_menu(driver)
    driver.find_element(By.ID, "logout_sidebar_link").click()
    assert "index.html" in driver.current_url, "Did not redirect to login page after logout"

def test_about_button(driver):
    open_burger_menu(driver)
    driver.find_element(By.ID, "about_sidebar_link").click()
    # Verification here will depend on what the "About" link actually does.
    # For example, if it opens a new tab, you would switch to that tab and then verify the URL.
    about_window = driver.window_handles[-1]
    driver.switch_to.window(about_window)
    assert "about" in driver.current_url, "Did not navigate to 'About' page"

def test_reset_app_state(driver):
    open_burger_menu(driver)
    driver.find_element(By.CLASS_NAME, "inventory_item_name").click()
    driver.find_element(By.CLASS_NAME, "btn_inventory").click()  # Добавить товар в корзину
    open_burger_menu(driver)
    driver.find_element(By.ID, "reset_sidebar_link").click()
    open_burger_menu(driver)
    cart_items = driver.find_elements(By.CLASS_NAME, "inventory_item_name")
    assert len(cart_items) == 6, "App state was not reset"  # Подтверждаем, что в корзине нет товаров
