from selenium.webdriver.common.by import By
from data import *
from locators import *
import time
import pytest


@pytest.fixture
def test_start(driver):
    driver.get(main_page)
    assert driver.find_element(By.XPATH, h1).text == "Практика с ожиданиями в Selenium"
    """Дождаться появления кнопки "Начать тестирование"""
    time.sleep(10)
    start_testing_button = driver.find_element(By.XPATH, start_test_button)
    assert start_testing_button.text == 'Начать тестирование'
    """Найти кнопку: Найти на странице кнопку с текстом "Начать тестирование"."""
    """Начать тестирование: Кликнуть по кнопке "Начать тестирование"."""
    driver.find_element(By.XPATH, start_test_button).click()
    return driver


def test_auth(test_start):
    driver = test_start
    """Ввод логина: Ввести "login" в поле для логина."""
    driver.find_element(By.XPATH, login_field).send_keys(login)
    """Ввод пароля: Ввести "password" в поле для пароля."""
    driver.find_element(By.XPATH, password_field).send_keys(password)
    """Согласие с правилами: Установить флажок в чекбокс "Согласен со всеми правилами"."""
    driver.find_element(By.XPATH, agree_checkbox).click()
    """Подтвердить регистрацию: Нажать кнопку "Зарегистрироваться"."""
    assert driver.find_element(By.XPATH, register_button).is_enabled()
    driver.find_element(By.XPATH, register_button).click()
    """Проверка загрузки: Удостовериться, что появился индикатор загрузки."""
    assert driver.find_element(By.XPATH, loader).is_displayed()
    time.sleep(5)
    success = driver.find_element(By.XPATH, success_message)
    """Проверка сообщения: Убедиться, что после завершения загрузки появилось сообщение "Вы успешно зарегистрированы"."""
    assert success.text == "Вы успешно зарегистрированы!"