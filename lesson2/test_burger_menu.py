
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

# Локаторы
USERNAME_INPUT = (By.ID, "user-name")
PASSWORD_INPUT = (By.ID, "password")
LOGIN_BUTTON = (By.ID, "login-button")
BURGER_MENU_BTN = (By.ID, "react-burger-menu-btn")
LOGOUT_LINK = (By.ID, "logout_sidebar_link")
ABOUT_LINK = (By.ID, "about_sidebar_link")
RESET_APP_STATE_LINK = (By.ID, "reset_sidebar_link")
ERROR_MESSAGE = (By.CLASS_NAME, "error-message-container")

# Фикстура для инициализации драйвера
@pytest.fixture(scope="function")
def driver():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get("https://www.saucedemo.com/")
    yield driver
    driver.quit()

# Функция логина
def login(driver, username, password):
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(USERNAME_INPUT)).send_keys(username)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(PASSWORD_INPUT)).send_keys(password)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(LOGIN_BUTTON)).click()

# Тесты
def test_login_with_valid_credentials(driver):
    login(driver, "standard_user", "secret_sauce")
    assert "inventory.html" in driver.current_url, "Login failed with valid credentials"

def test_login_with_invalid_credentials(driver):
    login(driver, "user", "user")
    error_message = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(ERROR_MESSAGE)).text
    assert "Username and password do not match any user in this service" in error_message, "Login didn't fail with invalid credentials"

def test_logout(driver):
    login(driver, "standard_user", "secret_sauce")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(BURGER_MENU_BTN)).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(LOGOUT_LINK)).click()
    WebDriverWait(driver, 10).until(EC.visibility_of(LOGIN_BUTTON))

def test_about_button(driver):
    login(driver, "standard_user", "secret_sauce")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(BURGER_MENU_BTN)).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(ABOUT_LINK)).click()
    # Добавить ассерт для проверки URL

def test_reset_app_state(driver):
    login(driver, "standard_user", "secret_sauce")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(BURGER_MENU_BTN)).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(RESET_APP_STATE_LINK)).click()
    # Добавить ассерт для проверки состояния корзины