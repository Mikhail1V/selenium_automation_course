import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Chrome()  # Можно указать путь к WebDriver, если он не в PATH
    driver.get("https://www.saucedemo.com/")
    login(driver)
    yield driver
    driver.quit()


def login(driver):
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()


def add_item_to_cart(driver):
    driver.find_element(By.CLASS_NAME, "btn_inventory").click()
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()


def test_checkout_with_valid_data(driver):
    add_item_to_cart(driver)
    driver.find_element(By.ID, "checkout").click()
    driver.find_element(By.ID, "first-name").send_keys("John")
    driver.find_element(By.ID, "last-name").send_keys("Doe")
    driver.find_element(By.ID, "postal-code").send_keys("12345")
    driver.find_element(By.ID, "continue").click()

    # Проверка, что находимся на странице подтверждения
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "finish")))
    driver.find_element(By.ID, "finish").click()

    # Проверка успешного оформления заказа
    success_message = driver.find_element(By.CLASS_NAME, "complete-header").text
    assert "THANK YOU FOR YOUR ORDER" in success_message, "Order was not completed successfully"