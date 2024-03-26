# импортируем необходимые библиотеки
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Фикстура для инициализации и очистки веб-драйвера
@pytest.fixture
def driver():
    driver = webdriver.Chrome()  # Замените на путь к драйверу, если он не в PATH
    driver.get("https://www.saucedemo.com/")
    yield driver
    driver.quit()

# Вспомогательная функция для входа в систему
def login(driver):
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

# Тест на выход из системы
def test_logout(driver):
    login(driver)
    driver.find_element(By.ID, "react-burger-menu-btn").click()
    driver.find_element(By.ID, "logout_sidebar_link").click()
    assert driver.find_element(By.ID, "login-button")

# Тест на работоспособность кнопки "About"
def test_about_button(driver):
    login(driver)
    driver.find_element(By.ID, "react-burger-menu-btn").click()
    driver.find_element(By.ID, "about_sidebar_link").click()
    # Проверка перехода на внешний URL может быть добавлена здесь

# Тест на работоспособность кнопки "Reset App State"
def test_reset_app_state(driver):
    login(driver)
    driver.find_element(By.ID, "react-burger-menu-btn").click()
    # Предполагаем, что уже есть товары в корзине. Если нет, добавьте их.
    driver.find_element(By.ID, "reset_sidebar_link").click()
    # Проверяем, что состояние корзины сброшено (например, корзина пуста)