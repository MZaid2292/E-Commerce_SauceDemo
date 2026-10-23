import pytest
from playwright.sync_api import expect
from pages.inventory_page import InventoryPage
from utils.config import BASE_URL

pytestmark = [pytest.mark.login, pytest.mark.regression]


def test_logout_returns_to_login_page(logged_in_page):
    InventoryPage(logged_in_page).logout()

    expect(logged_in_page).to_have_url(f"{BASE_URL}/")
    expect(logged_in_page.locator("[data-test='login-button']")).to_be_visible()


def test_inventory_blocked_after_logout(logged_in_page):
    InventoryPage(logged_in_page).logout()
    logged_in_page.goto(f"{BASE_URL}/inventory.html")

    error = logged_in_page.locator("[data-test='error']")
    expect(error).to_contain_text("You can only access '/inventory.html' when you are logged in")