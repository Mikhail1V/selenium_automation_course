import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Chrome()  # Указать путь до вашего WebDriver, если он не в PATH
    driver.get("https://www.saucedemo.com/")
    login(driver)
    yield driver
    driver.quit()

def login(driver):
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

def test_transition_by_clicking_image(driver):
    driver.find_elements(By.CLASS_NAME, "inventory_item_img")[0].click()
    assert "inventory-item.html" in driver.current_url, "Did not transition to product card after clicking image"

def test_transition_by_clicking_title(driver):
    driver.find_elements(By.CLASS_NAME, "inventory_item_name")[0].click()
    assert "inventory-item.html" in driver.current_url, "Did not transition to product card after clicking title"
