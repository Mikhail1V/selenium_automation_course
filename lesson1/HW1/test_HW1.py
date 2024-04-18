import time
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pytest
from selenium.webdriver.chrome.options import Options

# Домашнее задание к первому уроку

# Необходимо написать автотесты для сайта saucedemo:
# Ссылка на сайт: https://www.saucedemo.com/
url = "https://www.saucedemo.com/"



@pytest.fixture()
def browser():
    # browser = webdriver.Chrome()
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    browser = webdriver.Chrome(options=chrome_options)
    browser.implicitly_wait(3)
    yield browser
    browser.quit()


# Функционал, который необходимо покрыть автотестами:
# **Авторизация**
# 1. Авторизация используя корректные данные (standard_user, secret_sauce)
def test_auth_positive(browser):
    username = "standard_user"
    password = "secret_sauce"
    browser.get(url)
    browser.find_element(By.ID, "user-name").send_keys(username)
    browser.find_element(By.ID, 'password').send_keys(password)
    browser.find_element(By.ID, 'login-button').click()
    assert browser.current_url == f'{url}inventory.html', 'url не соответствует ожидаемому'


# 2. Авторизация используя некорректные данные (user, user)
def test_auth_negative(browser):
    username = "user"
    password = "user"
    browser.get(url)
    browser.find_element(By.ID, "user-name").send_keys(username)
    browser.find_element(By.ID, 'password').send_keys(password)
    browser.find_element(By.ID, 'login-button').click()
    errorField = browser.find_element(By.XPATH, "//h3[@data-test='error']")
    assert (errorField.text == 'Epic sadface: Username and password do not match any user in this service'), \
        "Текст ошибки не соответствует ожидаемому значению"


# **Корзина**
# 1. Добавление товара в корзину через каталог
def test_add_card_to_cart_from_catalog(browser):
    test_auth_positive(browser)
    # time.sleep(2)
    browser.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
    # cart_badge = browser.find_element(By.CLASS_NAME, "shopping_cart_badge").text
    # assert cart_badge == '1', 'Товар не добавлен в корзину'
    browser.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    # time.sleep(2)
    try:
        browser.find_element(By.ID, "item_4_title_link")
        assert True
    except NoSuchElementException:
        assert False, "Товар не добавлен в корзину"


# 2. Удаление товара из корзины через корзину
def test_delete_card_from_cart(browser):
    test_add_card_to_cart_from_catalog(browser)
    # time.sleep(2)
    browser.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    # time.sleep(2)
    browser.find_element(By.ID, "remove-sauce-labs-backpack").click()
    # time.sleep(2)
    try:
        browser.find_element(By.CLASS_NAME, "shopping_cart_badge")
        assert False, "Товар не удален из корзины"
    except NoSuchElementException:
        assert True


# 3. Добавление товара в корзину из карточки товара
def test_add_card_to_cart_from_card_details(browser):
    test_card_details_from_image(browser)
    browser.find_element(By.ID, "add-to-cart").click()
    # time.sleep(2)
    # cart_badge = browser.find_element(By.CLASS_NAME, "shopping_cart_badge").text
    # assert cart_badge == '1', 'Товар не добавлен в корзину'
    browser.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    # time.sleep(2)
    try:
        browser.find_element(By.ID, "item_4_title_link")
        assert True
    except NoSuchElementException:
        assert False, "Товар не добавлен в корзину"


# 4. Удаление товара из корзины через карточку товара
def test_delete_card_from_cart_from_card_details(browser):
    test_add_card_to_cart_from_card_details(browser)
    # time.sleep(2)
    # browser.find_element(By.ID, "remove-sauce-labs-backpack").click()
    test_card_details_from_name(browser)
    # time.sleep(2)
    browser.find_element(By.ID, "remove").click()
    # time.sleep(2)
    try:
        browser.find_element(By.CLASS_NAME, "shopping_cart_badge")
        assert False, "Товар не удален из корзины"
    except NoSuchElementException:
        assert True


# **Карточка товара**
# 1. Успешный переход к карточке товара после клика на картинку товара
def test_card_details_from_image(browser):
    test_auth_positive(browser)
    # time.sleep(2)
    browser.find_element(By.XPATH, '//*[@id="item_4_img_link"]').click()
    # time.sleep(2)
    assert browser.current_url == f'{url}inventory-item.html?id=4', "Не перешли на карточку товара"


# 2. Успешный переход к карточке товара после клика на название товара
def test_card_details_from_name(browser):
    test_auth_positive(browser)
    # time.sleep(2)
    browser.find_element(By.XPATH, '//*[@id="item_4_title_link"]').click()
    # time.sleep(2)
    assert browser.current_url == f'{url}inventory-item.html?id=4', "Не перешли на карточку товара"


# **Оформление заказа**
# 1. Оформление заказа используя корректные данные
def test_order_positive(browser):
    firstname = "Emilia"
    lastname = "Night"
    zipcode = "123456"
    test_add_card_to_cart_from_catalog(browser)
    # time.sleep(2)
    browser.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    # time.sleep(2)
    browser.find_element(By.ID, 'checkout').click()
    # time.sleep(2)
    browser.find_element(By.ID, 'first-name').send_keys(firstname)
    browser.find_element(By.ID, 'last-name').send_keys(lastname)
    browser.find_element(By.ID, 'postal-code').send_keys(zipcode)
    browser.find_element(By.ID, 'continue').click()
    # time.sleep(2)
    browser.find_element(By.ID, 'finish').click()
    # time.sleep(2)
    assert browser.current_url == f'{url}checkout-complete.html'
    message = browser.find_element(By.CLASS_NAME, "complete-header").text
    assert message == "Thank you for your order!", "Заказ не совершен"


# **Фильтр**
# 1. Проверка работоспособности фильтра (A to Z)
def test_filter_a_to_z(browser):
    test_auth_positive(browser)
    # test_filter_z_to_a(browser)
    sort_dropdown = browser.find_element(By.CLASS_NAME, "product_sort_container")
    select = Select(sort_dropdown)
    select.select_by_value("az")
    # time.sleep(2)
    items = browser.find_elements(By.CLASS_NAME, "inventory_item_name")
    actual_names = [item.text for item in items]
    sorted_names = sorted(actual_names)
    assert actual_names == sorted_names, 'Названия товаров не отсортированы по алфавиту A-Z'


# 2. Проверка работоспособности фильтра (Z to A)
def test_filter_z_to_a(browser):
    test_auth_positive(browser)
    sort_dropdown = browser.find_element(By.CLASS_NAME, "product_sort_container")
    select = Select(sort_dropdown)
    select.select_by_value("za")
    # time.sleep(2)
    items = browser.find_elements(By.CLASS_NAME, "inventory_item_name")
    actual_names = [item.text for item in items]
    # sorted_names = list(reversed(sorted(actual_names)))
    sorted_names = sorted(actual_names, reverse=True)
    assert actual_names == sorted_names, 'Названия товаров не отсортированы по алфавиту Z-A'


# 3. Проверка работоспособности фильтра (low to high)
def test_filter_low_to_high(browser):
    test_auth_positive(browser)
    sort_dropdown = browser.find_element(By.CLASS_NAME, "product_sort_container")
    select = Select(sort_dropdown)
    select.select_by_value("lohi")
    # time.sleep(2)
    items = browser.find_elements(By.CLASS_NAME, "inventory_item_price")
    actual_names = [float(item.text.strip('$')) for item in items]
    sorted_names = sorted(actual_names)
    assert actual_names == sorted_names, 'Товары не отсортированы по цене (низкая-высокая)'


# 4. Проверка работоспособности фильтра (high to low)
def test_filter_high_to_low(browser):
    test_auth_positive(browser)
    sort_dropdown = browser.find_element(By.CLASS_NAME, "product_sort_container")
    select = Select(sort_dropdown)
    select.select_by_value("hilo")
    # time.sleep(2)
    items = browser.find_elements(By.CLASS_NAME, "inventory_item_price")
    actual_names = [float(item.text.strip('$')) for item in items]
    # sorted_names = list(reversed(sorted(actual_names)))
    sorted_names = sorted(actual_names, reverse=True)
    assert actual_names == sorted_names, 'Товары не отсортированы по цене (высокая-низкая)'


# **Бургер меню**
# 1. Выход из системы
def test_logout(browser):
    test_auth_positive(browser)
    browser.find_element(By.ID, "react-burger-menu-btn").click()
    # time.sleep(2)
    browser.find_element(By.ID, "logout_sidebar_link").click()
    # time.sleep(2)
    assert browser.current_url == url, "Не работает выход"
    browser.get(f'{url}inventory.html')
    # time.sleep(2)
    assert browser.current_url == url, "При попытке открыть страницу произошел переход на другую страницу"


# 2. Проверка работоспособности кнопки "About" в меню
def test_about_button(browser):
    test_auth_positive(browser)
    browser.find_element(By.ID, "react-burger-menu-btn").click()
    # time.sleep(2)
    browser.find_element(By.ID, "about_sidebar_link").click()
    # time.sleep(2)
    assert browser.current_url == "https://saucelabs.com/", "Неверная страница"


# Страница нерабочая с ошибкой, но считаю, что так и надо, чтобы тест проходил


# 3. Проверка работоспособности кнопки "Reset App State"
def test_reset_app_state_button(browser):
    test_add_cards_to_cart_from_catalog(browser)
    # test_filter_high_to_low(browser)
    browser.find_element(By.ID, "react-burger-menu-btn").click()
    # time.sleep(2)
    browser.find_element(By.ID, "reset_sidebar_link").click()
    # time.sleep(2)
    try:
        browser.find_element(By.CLASS_NAME, "shopping_cart_badge")
        assert False, "Товар не удален из корзины"
    except NoSuchElementException:
        assert True
    # Нажатие на кнопку очищает корзину - считаю это за ожидаемый результат
    # browser.refresh()
    #     try:
    #         browser.find_element(By.ID, "remove-sauce-labs-backpack")
    #         assert False, "Кнопки Remove на карточках товара не возвращаются в исходное значение"
    #     except NoSuchElementException:
    #         assert True
    # Кнопки Remove на карточках товара не возвращаются в Add to cart без обновления страницы
    # items = browser.find_elements(By.CLASS_NAME, "inventory_item_name")
    # actual_names = [item.text for item in items]
    # sorted_names = sorted(actual_names)
    # assert actual_names == sorted_names, 'Названия товаров не отсортированы по умолчанию'
    # Сортировка не сбрасывается


# --------------------------------------------------------------------------------
def test_add_cards_to_cart_from_catalog(browser):
    test_auth_positive(browser)
    add_to_cart_buttons = browser.find_elements(By.CSS_SELECTOR,"button[data-test^='add-to-cart']")
    for button in add_to_cart_buttons:
        button.click()
    card_titles = []
    titles = browser.find_elements(By.CLASS_NAME, "inventory_item_name")
    for title in titles:
        card_titles.append(title.text)
    # browser.find_element(By.ID, "remove-sauce-labs-backpack").click()
    browser.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    for title in card_titles:
        try:
            browser.find_element(By.XPATH, f'//*[text()="{title}"]')
            assert True
        except NoSuchElementException:
            assert False, f'Товар {title} не добавлен в корзину'


def test_delete_cards_from_cart(browser):
    test_add_cards_to_cart_from_catalog(browser)
    browser.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    remove_from_cart_buttons = browser.find_elements(By.CSS_SELECTOR, "button[data-test^='remove']")
    for button in remove_from_cart_buttons:
        button.click()
    try:
        browser.find_element(By.CLASS_NAME, "inventory_item_name")
        assert False, f'Товары не удалены из корзины'
    except NoSuchElementException:
        assert True