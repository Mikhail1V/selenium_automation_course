import time
from random import *

from selenium.webdriver.support import expected_conditions as EC

from assert_messages import *
from locators import *


# Необходимо написать 3 автотеста для данной страницы:
# С использованием Explicit waits и Expected Conditions
def test_registration_functionality_with_explicit_waits(driver, wait):
    driver.get(main_url)
    title = wait.until(EC.visibility_of_element_located(head_title))
    assert title.text == expected_head_title, assert_head_title
    wait.until(EC.element_to_be_clickable(driver.find_element(*start_test_button))).click()
    login_input = wait.until(EC.visibility_of_element_located(login_field))
    login_input.send_keys(login)
    password_input = wait.until(EC.visibility_of_element_located(password_field))
    password_input.send_keys(password)
    checkbox_agree = wait.until(EC.visibility_of_element_located(agree_checkbox))
    checkbox_agree.click()
    assert checkbox_agree.is_selected()
    wait.until(EC.element_to_be_clickable(register_button)).click()
    assert check_exists(driver, loader), assert_loader_exist
    wait.until(EC.visibility_of_element_located(success_message))
    assert (check_exists(driver, success_message) and
            driver.find_element(*success_message).text == expected_success_message and
            not check_exists(driver, loader)), assert_success_message


# С использованием Implicit waits
def test_registration_functionality_with_implicit_waits(browser):
    browser.get(main_url)
    assert browser.find_element(*head_title).text == expected_head_title, assert_head_title
    browser.find_element(*start_test_button).click()
    browser.find_element(*login_field).send_keys(login)
    browser.find_element(*password_field).send_keys(password)
    checkbox_agree = browser.find_element(*agree_checkbox)
    checkbox_agree.click()
    assert checkbox_agree.is_selected()
    browser.find_element(*register_button).click()
    assert check_exists(browser, loader), assert_loader_exist
    time.sleep(4)
    assert (check_exists(browser, success_message) and
            browser.find_element(*success_message).text == expected_success_message and
            not check_exists(browser, loader)), assert_success_message


# С использованием time.sleep()
def test_registration_functionality_with_time_sleep(driver):
    driver.get(main_url)
    assert driver.find_element(*head_title).text == expected_head_title, assert_head_title
    time.sleep(5)
    driver.find_element(*start_test_button).click()
    driver.find_element(*login_field).send_keys(login)
    driver.find_element(*password_field).send_keys(password)
    checkbox_agree = driver.find_element(*agree_checkbox)
    checkbox_agree.click()
    assert checkbox_agree.is_selected()
    driver.find_element(*register_button).click()
    assert check_exists(driver, loader), assert_loader_exist
    time.sleep(4)
    assert (driver.find_element(*success_message).text == expected_success_message and
            not check_exists(driver, loader)), assert_success_message


# ---------------------------------------------------------------

# Так же необходимо написать несколько автотестов для сайта https://the-internet.herokuapp.com/ опираясь на
# полученные знания и поиск в интернете новой информации.
# https://the-internet.herokuapp.com/add_remove_elements/ (Необходимо создать и удалить элемент)
def test_add_delete_element(browser):
    browser.get(add_delete_element_url)
    assert not check_exists(browser, delete_button), assert_delete_button_exist
    count_of_buttons = randint(2, 20)
    for i in range(count_of_buttons):
        browser.find_element(*add_button).click()
    delete_buttons = browser.find_elements(*delete_button)
    assert (l := len(delete_buttons)) == count_of_buttons, assert_count_delete_button_exist.format(count_of_buttons, l)
    for button in delete_buttons:
        button.click()
    assert not check_exists(browser, delete_button), assert_delete_button_exist


# https://the-internet.herokuapp.com/basic_auth (Необходимо пройти базовую авторизацию)
def test_basic_auth(browser):
    browser.get(basic_auth_url)
    browser.get(f"https://{base_login}:{base_login}@the-internet.herokuapp.com/basic_auth/")
    assert (check_exists(browser, base_auth_message) and browser.find_element(*base_auth_message).text ==
            base_auth_text), assert_base_auth_message


# https://the-internet.herokuapp.com/broken_images (Необходимо найти сломанные изображения)
def test_broken_images(browser):
    browser.get(broken_images_url)
    all_images = browser.find_elements(*images)
    broken_images = []
    all_images_urls = []
    for img in all_images:
        all_images_urls.append(img.get_attribute("src"))
    for url in all_images_urls:
        browser.get(url)
        if not check_exists(browser, images):
            broken_images.append(url)
    print(broken_images)
    assert broken_images == broken_images_links, assert_broken_images


# https://the-internet.herokuapp.com/checkboxes (Практика с чек боксами)
def test_checkboxes(browser):
    browser.get(checkboxes_url)
    assert check_exists(browser, checkbox1) and check_exists(browser, checkbox2)
    check_box1 = browser.find_element(*checkbox1)
    check_box2 = browser.find_element(*checkbox2)
    assert not check_box1.is_selected() and check_box2.is_selected()
    check_box1.click()
    check_box2.click()
    assert check_exists(browser, checkbox1) and check_box1.is_selected()
    assert check_exists(browser, checkbox2) and not check_box2.is_selected()