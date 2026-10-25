from pages.base_page import BasePage

class InventoryPage(BasePage):
    URL_PATH = "/inventory.html"

    TITLE = "[data-test='title']"
    ITEMS = "[data-test='inventory-item']"
    ITEM_NAMES = "[data-test='inventory-item-name']"
    ITEM_PRICES = "[data-test='inventory-item-price']"
    SORT_DROPDOWN = "[data-test='product-sort-container']"

    CART_BADGE = "[data-test='shopping-cart-badge']"
    CART_LINK = "[data-test='shopping-cart-link']"

    def get_title(self):
        return self.page.locator(self.TITLE).inner_text()

    def get_item_count(self):
        return self.get_count(self.ITEMS)

    def get_item_names(self):
        return self.get_all_texts(self.ITEM_NAMES)

    def get_item_prices(self):
        texts = self.get_all_texts(self.ITEM_PRICES)
        return [float(t.replace("$", "")) for t in texts]

    def sort_by(self,option):
        self.page.select_option(self.SORT_DROPDOWN, option)

    def product_card(self, name):
        return self.page.locator(self.ITEMS).filter(has_text=name)

    def product_button(self, name):
        return self.product_card(name).locator("button")

    def add_to_cart(self, name):
        self.product_card(name).get_by_role("button", name="Add to cart").click()

    def remove_from_cart(self, name):
        self.product_card(name).get_by_role("button", name="Remove").click()

    def get_cart_count(self):
        badge = self.page.locator(self.CART_BADGE)
        return int(badge.inner_text()) if badge.count() > 0 else 0

    def open_cart(self):
        self.page.locator(self.CART_LINK).click()
        self.page.wait_for_url("**/cart.html")    