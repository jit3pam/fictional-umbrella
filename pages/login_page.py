from selenium.webdriver.common.by import By

from core.base_page import BasePage
from core.locator import Locator


class LoginPage(BasePage):
    PATH = "/login"

    USERNAME = Locator(By.ID, "username", "Username Input")
    PASSWORD = Locator(By.ID, "password", "Password Input")
    LOGIN_BUTTON = Locator(By.CSS_SELECTOR, "button[type='submit']", "Login Button")

    def open(self) -> None:
        self.driver.get(f"{self.base_url}{self.PATH}")

    def login(self, username: str, password: str) -> None:
        self.do(self.input(self.USERNAME), "type", username)
        self.do(self.input(self.PASSWORD), "type", password)
        self.do(self.button(self.LOGIN_BUTTON), "click")
