from selenium.webdriver.common.by import By
from selenium.common import NoSuchElementException


def check_exists(browser, selector):
    try:
        browser.find_element(*selector)
    except NoSuchElementException:
        return False
    return True


# AUTH
username_field = (By.ID, "user-name")
password_field = (By.ID, "password")
login_button = (By.ID, "login-button")
error_message = (By.XPATH, "//h3[@data-test='error']")

# CATALOG
add_to_cart_button = (By.ID, "add-to-cart-sauce-labs-backpack")
remove_from_cart_button = (By.ID, "remove-sauce-labs-backpack")

image_link_to_card = (By.ID, "item_4_img_link")
title_link_to_card = (By.ID, "item_4_title_link")

item_names = (By.CLASS_NAME, "inventory_item_name")
item_prices = (By.CLASS_NAME, "inventory_item_price")

add_to_cart_buttons = (By.CSS_SELECTOR, "button[data-test^='add-to-cart']")


def get_element_locator(text):
    return (By.XPATH, f"//*[text()='{text}']")


remove_all_from_cart_buttons = (By.CSS_SELECTOR, "button[data-test^='remove']")

# CARD
add_from_card_to_cart_button = (By.ID, "add-to-cart")
remove_from_card_from_cart_button = (By.ID, "remove")

# CART
number_in_cart = (By.CLASS_NAME, "shopping_cart_badge")
shopping_cart_link = (By.CLASS_NAME, "shopping_cart_link")

# ORDER
order_checkout_button = (By.ID, "checkout")
order_firstname_field = (By.ID, "first-name")
order_lastname_field = (By.ID, "last-name")
order_zipcode_field = (By.ID, "postal-code")
order_continue_button = (By.ID, "continue")
order_finish_button = (By.ID, "finish")
order_complete_message = (By.CLASS_NAME, "complete-header")

# SORT
selector_sorting = (By.CLASS_NAME, "product_sort_container")

# BURGER MENU
burger_menu_button = (By.ID, "react-burger-menu-btn")
about_link_button = (By.ID, "about_sidebar_link")
logout_button = (By.ID, "logout_sidebar_link")
reset_button = (By.ID, "reset_sidebar_link")

# REGISTRATION FORM
reg_username_field = (By.ID, "username")
reg_password_field = (By.ID, "password")
reg_checkbox = (By.ID, "agreement")
reg_register_button = (By.ID, "registerButton")