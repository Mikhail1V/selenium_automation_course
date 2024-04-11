from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class MainPage:
    START_TESTING_BUTTON_XPATH = "//button[text()='Начать тестирование']"
    USERNAME_INPUT_XPATH = "//input[@id='login']"
    PASSWORD_INPUT_XPATH = "//input[@id='password']"
    AGREE_CHECKBOX_XPATH = "//input[@id='agree']"
    REGISTER_BUTTON_XPATH = "//button[@id='register']"
    LOADING_INDICATOR_XPATH = "//div[@id='loader']"
    SUCCESS_MESSAGE_XPATH = "//div[@id='finish']/h4"

    def __init__(self, driver):
        self.driver = driver

    def start_testing(self):
        self.driver.find_element(By.XPATH, self.START_TESTING_BUTTON_XPATH).click()

    def register(self, username, password):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, self.USERNAME_INPUT_XPATH))
        ).send_keys(username)

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, self.PASSWORD_INPUT_XPATH))
        ).send_keys(password)

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, self.AGREE_CHECKBOX_XPATH))
        ).click()

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, self.REGISTER_BUTTON_XPATH))
        ).click()

    def await_registration_success(self):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, self.LOADING_INDICATOR_XPATH))
        )
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, self.SUCCESS_MESSAGE_XPATH))
        ).text
