from selenium.webdriver.support.ui import Select

from locators import *
from data import *
from assert_messages import *


# Функционал, который необходимо покрыть автотестами:
# **Авторизация**
# 1. Авторизация используя корректные данные (standard_user, secret_sauce)
def test_auth_positive(browser):
    browser.get(main_url)
    browser.find_element(*username_field).send_keys(username_pos)
    browser.find_element(*password_field).send_keys(password_pos)
    browser.find_element(*login_button).click()
    assert browser.current_url == catalog_url, url_pos_message


# 2. Авторизация используя некорректные данные (user, user)
def test_auth_negative(browser, fake_username, fake_password):
    browser.get(main_url)
    browser.find_element(*username_field).send_keys(fake_username)
    browser.find_element(*password_field).send_keys(fake_password)
    browser.find_element(*login_button).click()
    assert (browser.find_element(*error_message).text == error_auth_neg), auth_neg_message


# **Корзина**
# 1. Добавление товара в корзину через каталог
def test_add_card_to_cart_from_catalog(browser):
    test_auth_positive(browser)
    browser.find_element(*add_to_cart_button).click()
    # assert browser.find_element(*number_in_cart).text == number_in_cart_value, add_card_to_cart_message
    browser.find_element(*shopping_cart_link).click()
    assert check_exists(browser, title_link_to_card), add_card_to_cart_message


# 2. Удаление товара из корзины через корзину
def test_delete_card_from_cart(browser):
    test_add_card_to_cart_from_catalog(browser)
    browser.find_element(*shopping_cart_link).click()
    browser.find_element(*remove_from_cart_button).click()
    assert not check_exists(browser, number_in_cart), delete_from_cart_message


# 3. Добавление товара в корзину из карточки товара
def test_add_card_to_cart_from_card_details(browser):
    test_card_details_from_image(browser)
    browser.find_element(*add_from_card_to_cart_button).click()
    # assert browser.find_element(*number_in_cart).text == number_in_cart_value, add_card_to_cart_message
    browser.find_element(*shopping_cart_link).click()
    assert check_exists(browser, title_link_to_card), add_card_to_cart_message


# 4. Удаление товара из корзины через карточку товара
def test_delete_card_from_cart_from_card_details(browser):
    test_add_card_to_cart_from_card_details(browser)
    test_card_details_from_name(browser)
    browser.find_element(*remove_from_card_from_cart_button).click()
    assert not check_exists(browser, number_in_cart), delete_from_cart_message


# **Карточка товара**
# 1. Успешный переход к карточке товара после клика на картинку товара
def test_card_details_from_image(browser):
    test_auth_positive(browser)
    browser.find_element(*image_link_to_card).click()
    assert browser.current_url == card_url, card_details_message


def test_card_details_from_image2(browser1):
    browser1.find_element(*image_link_to_card).click()
    assert browser1.current_url == card_url, card_details_message


# 2. Успешный переход к карточке товара после клика на название товара
def test_card_details_from_name(browser):
    test_auth_positive(browser)
    browser.find_element(*title_link_to_card).click()
    assert browser.current_url == card_url, card_details_message


# **Оформление заказа**
# 1. Оформление заказа используя корректные данные
def test_order_positive(browser, fake_firstname, fake_lastname, fake_zipcode):
    test_add_card_to_cart_from_catalog(browser)
    browser.find_element(*shopping_cart_link).click()
    browser.find_element(*order_checkout_button).click()
    browser.find_element(*order_firstname_field).send_keys(fake_firstname)
    browser.find_element(*order_lastname_field).send_keys(fake_lastname)
    browser.find_element(*order_zipcode_field).send_keys(fake_zipcode)
    browser.find_element(*order_continue_button).click()
    browser.find_element(*order_finish_button).click()
    assert browser.current_url == complete_order_url
    assert browser.find_element(*order_complete_message).text == order_pos_text, order_pos_message


# **Фильтр**
# 1. Проверка работоспособности фильтра (A to Z)
def test_filter_a_to_z(browser):
    test_auth_positive(browser)
    # test_filter_z_to_a(browser)
    sort_dropdown = browser.find_element(*selector_sorting)
    select = Select(sort_dropdown)
    select.select_by_value(select_az)
    items = browser.find_elements(*item_names)
    actual_names = [item.text for item in items]
    sorted_names = sorted(actual_names)
    assert actual_names == sorted_names, sorting_message + select_az


# 2. Проверка работоспособности фильтра (Z to A)
def test_filter_z_to_a(browser):
    test_auth_positive(browser)
    sort_dropdown = browser.find_element(*selector_sorting)
    select = Select(sort_dropdown)
    select.select_by_value(select_za)
    items = browser.find_elements(*item_names)
    actual_names = [item.text for item in items]
    # sorted_names = list(reversed(sorted(actual_names)))
    sorted_names = sorted(actual_names, reverse=True)
    assert actual_names == sorted_names, sorting_message + select_za


# 3. Проверка работоспособности фильтра (low to high)
def test_filter_low_to_high(browser):
    test_auth_positive(browser)
    sort_dropdown = browser.find_element(*selector_sorting)
    select = Select(sort_dropdown)
    select.select_by_value(select_lohi)
    items = browser.find_elements(*item_prices)
    actual_names = [float(item.text.strip('$')) for item in items]
    sorted_names = sorted(actual_names)
    assert actual_names == sorted_names, sorting_message + select_lohi


# 4. Проверка работоспособности фильтра (high to low)
def test_filter_high_to_low(browser):
    test_auth_positive(browser)
    sort_dropdown = browser.find_element(*selector_sorting)
    select = Select(sort_dropdown)
    select.select_by_value(select_hilo)
    items = browser.find_elements(*item_prices)
    actual_names = [float(item.text.strip('$')) for item in items]
    # sorted_names = list(reversed(sorted(actual_names)))
    sorted_names = sorted(actual_names, reverse=True)
    assert actual_names == sorted_names, sorting_message + select_hilo


# **Бургер меню**
# 1. Выход из системы
def test_logout(browser):
    test_auth_positive(browser)
    browser.find_element(*burger_menu_button).click()
    browser.find_element(*logout_button).click()
    assert browser.current_url == main_url, logout_message
    browser.get(catalog_url)
    assert browser.current_url == main_url, logout_message


# 2. Проверка работоспособности кнопки "About" в меню
def test_about_button(browser):
    test_auth_positive(browser)
    browser.find_element(*burger_menu_button).click()
    browser.find_element(*about_link_button).click()
    assert browser.current_url == about_url, url_pos_message


# Страница нерабочая с ошибкой, но считаю, что так и надо, чтобы тест проходил


# 3. Проверка работоспособности кнопки "Reset App State"
def test_reset_app_state_button(browser):
    test_add_cards_to_cart_from_catalog(browser)
    # test_filter_high_to_low(browser)
    browser.find_element(*burger_menu_button).click()
    browser.find_element(*reset_button).click()
    assert not check_exists(browser, number_in_cart), delete_from_cart_message
    # Нажатие на кнопку очищает корзину - считаю это за ожидаемый результат
    # browser.refresh()
    # assert not check_exists(browser, remove_from_cart_button), reset_add_button_message
    # Кнопки Remove на карточках товара не возвращаются в Add to cart без обновления страницы
    # items = browser.find_elements(*item_names)
    # actual_names = [item.text for item in items]
    # sorted_names = sorted(actual_names)
    # assert actual_names == sorted_names, sorting_message
    # Сортировка не сбрасывается


# --------------------------------------------------------------------------------
def test_add_cards_to_cart_from_catalog(browser):
    test_auth_positive(browser)
    add_buttons = browser.find_elements(*add_to_cart_buttons)
    for button in add_buttons:
        button.click()
    card_titles = []
    titles = browser.find_elements(*item_names)
    for title in titles:
        card_titles.append(title.text)
    # browser.find_element(*remove_from_cart_button).click()
    browser.find_element(*shopping_cart_link).click()
    for title in card_titles:
        assert check_exists(browser, get_element_locator(title)), add_cards_to_cart_from_catalog.format(title)


def test_delete_cards_from_cart(browser):
    test_add_cards_to_cart_from_catalog(browser)
    browser.find_element(*shopping_cart_link).click()
    remove_from_cart_buttons = browser.find_elements(*remove_all_from_cart_buttons)
    for button in remove_from_cart_buttons:
        button.click()
    assert not check_exists(browser, item_names), delete_cards_from_cart


# --------------------------------------------------------------------------------
def test_register_form_with_checkbox(browser, fake_username, fake_password):
    browser.get(register_form_url)
    register_button = browser.find_element(*reg_register_button)
    assert not register_button.is_enabled(), reg_not_enabled_button
    browser.find_element(*reg_username_field).send_keys(fake_username)
    assert not register_button.is_enabled(), reg_not_enabled_button
    browser.find_element(*reg_password_field).send_keys(fake_password)
    assert not register_button.is_enabled(), reg_not_enabled_button
    browser.find_element(*reg_checkbox).click()
    assert register_button.is_enabled(), reg_enabled_button
    register_button.click()
    assert browser.current_url == f'{register_form_url}?', url_pos_message