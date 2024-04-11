import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# Локаторы
USERNAME_INPUT = (By.ID, "user-name")
PASSWORD_INPUT = (By.ID, "password")
LOGIN_BUTTON = (By.ID, "login-button")
ERROR_MESSAGE = (By.CLASS_NAME, "error-message-container")

# Тестовые данные
VALID_USERNAME = "standard_user"
VALID_PASSWORD = "secret_sauce"
INVALID_USERNAME = "user"
INVALID_PASSWORD = "user"

# Фикстура для инициализации драйвера
@pytest.fixture(scope="function")
def driver():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get("https://www.saucedemo.com/")
    yield driver
    driver.quit()

# Тест с валидными учетными данными
def test_login_with_valid_credentials(driver):
    driver.find_element(*USERNAME_INPUT).send_keys(VALID_USERNAME)
    driver.find_element(*PASSWORD_INPUT).send_keys(VALID_PASSWORD)
    driver.find_element(*LOGIN_BUTTON).click()
    assert "inventory.html" in driver.current_url, "Login failed with valid credentials"

# Тест с невалидными учетными данными
def test_login_with_invalid_credentials(driver):
    driver.find_element(*USERNAME_INPUT).send_keys(INVALID_USERNAME)
    driver.find_element(*PASSWORD_INPUT).send_keys(INVALID_PASSWORD)
    driver.find_element(*LOGIN_BUTTON).click()
    error_message = driver.find_element(*ERROR_MESSAGE).text
    assert ("Username and password do not match any user in this service"
            in error_message), "Login didn't fail with invalid credentials"