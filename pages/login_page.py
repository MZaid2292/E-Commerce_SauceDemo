from pages.base_page import BasePage

class LoginPage(BasePage):
    URL = "https://www.saucedemo.com/"

    USERNAME_INPUT = "#user-name"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "#login-button"

    PRODUCTS_CONTAINER = ".inventory_list"
    ERROR_MESSAGE = '[data-test="error"]'

    def open_login_page(self):
        self.open_url(self.URL)

    def login(self,username,password):
        self.fill_field(self.USERNAME_INPUT,username)
        self.fill_field(self.PASSWORD_INPUT,password)
        self.click_element(self.LOGIN_BUTTON)

    def is_products_page_visible(self):
        return self.is_visible(self.PRODUCTS_CONTAINER)

    def get_error_message(self):
        return self.get_text(self.ERROR_MESSAGE)        