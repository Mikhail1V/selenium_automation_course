import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Локаторы элементов на странице
USERNAME_INPUT = (By.ID, "user-name")
PASSWORD_INPUT = (By.ID, "password")
LOGIN_BUTTON = (By.ID, "login-button")
ADD_TO_CART_BUTTONS = (By.CLASS_NAME, "btn_inventory")
SHOPPING_CART_CONTAINER = (By.ID, "shopping_cart_container")
CHECKOUT_BUTTON = (By.ID, "checkout")
FIRST_NAME_INPUT = (By.ID, "first-name")
LAST_NAME_INPUT = (By.ID, "last-name")
POSTAL_CODE_INPUT = (By.ID, "postal-code")
CONTINUE_BUTTON = (By.ID, "continue")
FINISH_BUTTON = (By.ID, "finish")
ORDER_SUCCESS_MESSAGE = (By.CLASS_NAME, "complete-header")

# Тестовые данные
STANDARD_USER = "standard_user"
SECRET_SAUCE = "secret_sauce"
FIRST_NAME = "John"
LAST_NAME = "Doe"
POSTAL_CODE = "12345"


@pytest.fixture(scope="function")
def driver():
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(10)  # Устанавливаем неявное ожидание элементов
    driver.get("https://www.saucedemo.com/")
    yield driver
    driver.quit()


def test_checkout_with_valid_data(driver):
    # Вход в систему
    driver.find_element(*USERNAME_INPUT).send_keys(STANDARD_USER)
    driver.find_element(*PASSWORD_INPUT).send_keys(SECRET_SAUCE)
    driver.find_element(*LOGIN_BUTTON).click()

    # Добавление товара в корзину и его оформление
    driver.find_element(*ADD_TO_CART_BUTTONS).click()
    driver.find_element(*SHOPPING_CART_CONTAINER).click()
    driver.find_element(*CHECKOUT_BUTTON).click()

    # Ввод данных пользователя
    driver.find_element(*FIRST_NAME_INPUT).send_keys(FIRST_NAME)
    driver.find_element(*LAST_NAME_INPUT).send_keys(LAST_NAME)
    driver.find_element(*POSTAL_CODE_INPUT).send_keys(POSTAL_CODE)

    # Продолжение оформления и завершение покупки
    driver.find_element(*CONTINUE_BUTTON).click()
    driver.find_element(*FINISH_BUTTON).click()

    # Проверка успешного оформления заказа
    success_message = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(ORDER_SUCCESS_MESSAGE)).text
    assert "THANK YOU FOR YOUR ORDER" in success_message, "Order was not completed successfully."