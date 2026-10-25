from pages.base_page import BasePage


class CartPage(BasePage):
    TITLE = "[data-test='title']"
    CART_ITEMS = "[data-test='inventory-item']"
    ITEM_NAMES = "[data-test='inventory-item-name']"
    CONTINUE_SHOPPING = "[data-test='continue-shopping']"
    CHECKOUT_BUTTON = "[data-test='checkout']"

    def get_title(self):
        return self.page.locator(self.TITLE).inner_text()

    def get_item_count(self):
        return self.get_count(self.CART_ITEMS)

    def get_item_names(self):
        return self.get_all_texts(self.ITEM_NAMES)

    def remove_item(self, name):
        (
            self.page.locator(self.CART_ITEMS)
            .filter(has_text=name)
            .get_by_role("button", name="Remove")
            .click()
        )

    def continue_shopping(self):
        self.page.locator(self.CONTINUE_SHOPPING).click()

    def go_to_checkout(self):
        self.page.locator(self.CHECKOUT_BUTTON).click()