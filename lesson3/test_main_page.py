import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from main_page import MainPage


@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)  # Устанавливается глобальное ожидание
    driver.get("https://victoretc.github.io/selenium_waits/")
    return driver


def test_registration_using_xpath(driver):
    main_page = MainPage(driver)

    # Дождаться появления кнопки "Начать тестирование" и начать процесс регистрации
    main_page.start_testing()

    # Ввод логина и пароля, согласие с правилами и подтверждение регистрации
    main_page.register("new_user_login", "new_user_password")

    # Проверка появления индикатора загрузки и сообщения об успешной регистрации
    success_message = main_page.await_registration_success()
    assert "Вы успешно зарегистрированы" in success_message, "Сообщение о успешной регистрации не появилось"

def teardown_function(driver):
    driver.quit()
