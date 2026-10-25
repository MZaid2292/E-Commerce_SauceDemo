import pytest
from playwright.sync_api import expect
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import (
    CheckoutInfoPage, CheckoutOverviewPage, CheckoutCompletePage,
)
from utils.data_loader import load_json
from utils.config import BASE_URL

pytestmark = [pytest.mark.checkout, pytest.mark.regression]

DATA = load_json("checkout_data.json")
CUSTOMER = DATA["valid_customer"]

BACKPACK = "Sauce Labs Backpack"
BIKE_LIGHT = "Sauce Labs Bike Light"


def go_to_checkout(page, products):
    """Products cart mein daal ke checkout info page tak le jata hai."""
    inventory = InventoryPage(page)
    for product in products:
        inventory.add_to_cart(product)
    inventory.open_cart()
    CartPage(page).go_to_checkout()
    return CheckoutInfoPage(page)


@pytest.mark.parametrize(
    "case", DATA["invalid_info"], ids=[c["test_id"] for c in DATA["invalid_info"]]
)
def test_checkout_info_validation(logged_in_page, case):
    info = go_to_checkout(logged_in_page, [BACKPACK])
    info.fill_info(case["first_name"], case["last_name"], case["postal_code"])
    info.continue_checkout()

    assert info.get_error() == case["expected_error"]
    expect(logged_in_page).to_have_url(f"{BASE_URL}/checkout-step-one.html")


def test_overview_shows_items_and_correct_total(logged_in_page):
    info = go_to_checkout(logged_in_page, [BACKPACK, BIKE_LIGHT])
    info.fill_info(**{k: CUSTOMER[k] for k in ("first_name", "last_name", "postal_code")})
    info.continue_checkout()

    overview = CheckoutOverviewPage(logged_in_page)
    expect(logged_in_page).to_have_url(f"{BASE_URL}/checkout-step-two.html")
    expect(logged_in_page.locator(CheckoutOverviewPage.TITLE)).to_have_text("Checkout: Overview")
    assert sorted(overview.get_item_names()) == sorted([BACKPACK, BIKE_LIGHT])

    # subtotal = items ka sum, total = subtotal + tax
    assert overview.get_subtotal() == round(sum(overview.get_item_prices()), 2)
    assert overview.get_total() == round(overview.get_subtotal() + overview.get_tax(), 2)


@pytest.mark.smoke
def test_complete_order_end_to_end(logged_in_page):
    info = go_to_checkout(logged_in_page, [BACKPACK])
    info.fill_info(CUSTOMER["first_name"], CUSTOMER["last_name"], CUSTOMER["postal_code"])
    info.continue_checkout()
    CheckoutOverviewPage(logged_in_page).finish()

    complete = CheckoutCompletePage(logged_in_page)
    expect(logged_in_page).to_have_url(f"{BASE_URL}/checkout-complete.html")
    assert complete.get_header() == "Thank you for your order!"
    assert InventoryPage(logged_in_page).get_cart_count() == 0


def test_cancel_checkout_returns_to_cart(logged_in_page):
    info = go_to_checkout(logged_in_page, [BACKPACK])
    info.cancel()

    expect(logged_in_page).to_have_url(f"{BASE_URL}/cart.html")
    assert CartPage(logged_in_page).get_item_names() == [BACKPACK]