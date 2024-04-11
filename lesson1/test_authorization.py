import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Chrome()  # Укажите путь к WebDriver, если он не в PATH
    driver.get("https://www.saucedemo.com/")
    yield driver
    driver.quit()

def test_login_with_valid_credentials(driver):
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    assert "inventory.html" in driver.current_url, "Login failed with valid credentials"

def test_login_with_invalid_credentials(driver):
    driver.find_element(By.ID, "user-name").send_keys("user")
    driver.find_element(By.ID, "password").send_keys("user")
    driver.find_element(By.ID, "login-button").click()
    error_message = driver.find_element(By.CLASS_NAME, "error-message-container").text
    assert ("Username and password do not match any user in this service"
            in error_message), "Login didn't fail with invalid credentials"