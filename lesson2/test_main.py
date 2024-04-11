import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Локаторы
USERNAME_INPUT = (By.ID, "user-name")
PASSWORD_INPUT = (By.ID, "password")
LOGIN_BUTTON = (By.ID, "login-button")
INVENTORY_URL = "https://www.saucedemo.com/inventory.html"

# Тестовые данные
VALID_USERNAME = "standard_user"
VALID_PASSWORD = "secret_sauce"


# Фикстура для настройки и очистки драйвера
@pytest.fixture(scope="function")
def driver():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.implicitly_wait(10)  # Неявное ожидание для улучшения стабильности
    yield driver
    driver.quit()


@pytest.mark.parametrize('username, password', [(VALID_USERNAME, VALID_PASSWORD)])
def test_auth_positive(driver, username, password):
    # Открываем целевую страницу
    driver.get("https://www.saucedemo.com/")

    # Вводим данные авторизации и подтверждаем вход
    driver.find_element(*USERNAME_INPUT).send_keys(username)
    driver.find_element(*PASSWORD_INPUT).send_keys(password)
    driver.find_element(*LOGIN_BUTTON).click()

    # Выполняем проверку URL для подтверждения успешного входа
    assert driver.current_url == INVENTORY_URL, 'URL не соответствует ожидаемому после логина'