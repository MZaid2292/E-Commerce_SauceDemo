import pytest
from playwright.sync_api import expect
from pages.inventory_page import InventoryPage

pytestmark = [pytest.mark.inventory, pytest.mark.regression]

def test_inventory_page_loads(logged_in_page):
    inventory = InventoryPage(logged_in_page)
    expect(logged_in_page).to_have_url("https://www.saucedemo.com/inventory.html")
    expect(logged_in_page.locator(InventoryPage.TITLE)).to_have_text("Products")

def test_six_products_displayed(logged_in_page):
    inventory = InventoryPage(logged_in_page)
    assert inventory.get_item_count() == 6

def test_every_product_has_name_and_price(logged_in_page):
    inventory = InventoryPage(logged_in_page)
    names = inventory.get_item_names()
    prices = inventory.get_item_prices()

    assert len(names) == len(prices) == 6
    assert all(name.strip() for name in names)
    assert all(price > 0 for price in prices)

@pytest.mark.parametrize(
    "option, reverse",
    [("az", False), ("za", True)],
    ids=["name_a_to_z", "name_z_to_a"],
)
def test_sort_by_name(logged_in_page, option, reverse):
    inventory = InventoryPage(logged_in_page)
    inventory.sort_by(option)
    names = inventory.get_item_names()
    assert names == sorted(names, reverse=reverse)


@pytest.mark.parametrize(
    "option, reverse",
    [("lohi", False), ("hilo", True)],
    ids=["price_low_to_high", "price_high_to_low"],
)
def test_sort_by_price(logged_in_page, option, reverse):
    inventory = InventoryPage(logged_in_page)
    inventory.sort_by(option)
    prices = inventory.get_item_prices()
    assert prices == sorted(prices, reverse=reverse)