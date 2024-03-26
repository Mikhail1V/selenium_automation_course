import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Фикстура для настройки драйвера
@pytest.fixture
def driver():
    driver = webdriver.Chrome()  # Замените на путь к драйверу, если он не в PATH
    driver.implicitly_wait(10)  # Установим неявное ожидание
    driver.get("https://www.saucedemo.com/")
    yield driver
    driver.quit()


# Вспомогательная функция для авторизации
def login(driver):
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()


# Вспомогательная функция для добавления товара в корзину
def add_first_item_to_cart(driver):
    driver.find_element(By.CLASS_NAME, "btn_inventory").click()


# Тест оформления заказа
def test_checkout_with_valid_data(driver):
    login(driver)
    add_first_item_to_cart(driver)
    driver.find_element(By.ID, "shopping_cart_container").click()
    driver.find_element(By.ID, "checkout").click()
    driver.find_element(By.ID, "first-name").send_keys("John")
    driver.find_element(By.ID, "last-name").send_keys("Doe")
    driver.find_element(By.ID, "postal-code").send_keys("12345")
    driver.find_element(By.ID, "continue").click()
    driver.find_element(By.ID, "finish").click()

    # Проверка успешного оформления заказа
    success_message = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "complete-header"))
    )
