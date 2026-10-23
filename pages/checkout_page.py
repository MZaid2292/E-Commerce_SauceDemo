from pages.base_page import BasePage


def _amount(text):
    # "Item total: $39.98" -> 39.98
    return float(text.split("$")[1])


class CheckoutInfoPage(BasePage):
    FIRST_NAME = "[data-test='firstName']"
    LAST_NAME = "[data-test='lastName']"
    POSTAL_CODE = "[data-test='postalCode']"
    CONTINUE = "[data-test='continue']"
    CANCEL = "[data-test='cancel']"
    ERROR = "[data-test='error']"

    def fill_info(self, first_name, last_name, postal_code):
        self.page.locator(self.FIRST_NAME).fill(first_name)
        self.page.locator(self.LAST_NAME).fill(last_name)
        self.page.locator(self.POSTAL_CODE).fill(postal_code)

    def continue_checkout(self):
        self.page.locator(self.CONTINUE).click()

    def cancel(self):
        self.page.locator(self.CANCEL).click()

    def get_error(self):
        return self.page.locator(self.ERROR).inner_text()


class CheckoutOverviewPage(BasePage):
    TITLE = "[data-test='title']"
    ITEM_NAMES = "[data-test='inventory-item-name']"
    ITEM_PRICES = "[data-test='inventory-item-price']"
    SUBTOTAL = "[data-test='subtotal-label']"
    TAX = "[data-test='tax-label']"
    TOTAL = "[data-test='total-label']"
    FINISH = "[data-test='finish']"

    def get_title(self):
        return self.page.locator(self.TITLE).inner_text()

    def get_item_names(self):
        return self.page.locator(self.ITEM_NAMES).all_inner_texts()

    def get_item_prices(self):
        texts = self.page.locator(self.ITEM_PRICES).all_inner_texts()
        return [float(t.replace("$", "")) for t in texts]

    def get_subtotal(self):
        return _amount(self.page.locator(self.SUBTOTAL).inner_text())

    def get_tax(self):
        return _amount(self.page.locator(self.TAX).inner_text())

    def get_total(self):
        return _amount(self.page.locator(self.TOTAL).inner_text())

    def finish(self):
        self.page.locator(self.FINISH).click()


class CheckoutCompletePage(BasePage):
    HEADER = "[data-test='complete-header']"
    BACK_HOME = "[data-test='back-to-products']"

    def get_header(self):
        return self.page.locator(self.HEADER).inner_text()

    def back_home(self):
        self.page.locator(self.BACK_HOME).click()