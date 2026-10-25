from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

import logging

logger = logging.getLogger(__name__)


class BasePage:
    MENU_BUTTON = "#react-burger-menu-btn"
    LOGOUT_LINK = "#logout_sidebar_link"

    def __init__(self, page):
        self.page = page

    def open_url(self, url):
        logger.info(f"Opening URL: {url}")
        self.page.goto(url, wait_until="domcontentloaded", timeout=60000)

    def fill_field(self, locator, value):
        logger.info(f"Filling field: {locator}")
        self.page.locator(locator).fill(value)

    def click_element(self, locator):
        logger.info(f"Clicking: {locator}")
        self.page.locator(locator).click()

    def get_text(self, locator):
        return self.page.locator(locator).inner_text()

    def is_visible(self, locator, timeout=5000):
        """Element ke visible hone ka wait karta hai (max 5 sec)."""
        try:
            self.page.locator(locator).wait_for(state="visible", timeout=timeout)
            return True
        except PlaywrightTimeoutError:
            return False

    def logout(self):
        logger.info("Logging out")
        self.click_element(self.MENU_BUTTON)
        self.click_element(self.LOGOUT_LINK)

    def get_all_texts(self, locator):
        """Pehle item ke visible hone ka wait karta hai, phir saare texts deta hai."""
        items = self.page.locator(locator)
        items.first.wait_for(state="visible")
        return items.all_inner_texts()

    def get_count(self, locator):
        """Pehle item ke visible hone ka wait karta hai, phir count deta hai."""
        items = self.page.locator(locator)
        items.first.wait_for(state="visible")
        return items.count()    