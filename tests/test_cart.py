import pytest
from playwright.sync_api import expect
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage

pytestmark = [pytest.mark.cart, pytest.mark.regression]

BACKPACK = "Sauce Labs Backpack"
BIKE_LIGHT = "Sauce Labs Bike Light"
BOLT_SHIRT = "Sauce Labs Bolt T-Shirt"


def test_cart_is_empty_after_login(logged_in_page):
    inventory = InventoryPage(logged_in_page)
    assert inventory.get_cart_count() == 0


def test_add_single_item(logged_in_page):
    inventory = InventoryPage(logged_in_page)
    inventory.add_to_cart(BACKPACK)

    assert inventory.get_cart_count() == 1
    expect(inventory.product_button(BACKPACK)).to_have_text("Remove")


def test_add_multiple_items(logged_in_page):
    inventory = InventoryPage(logged_in_page)
    for product in [BACKPACK, BIKE_LIGHT, BOLT_SHIRT]:
        inventory.add_to_cart(product)

    assert inventory.get_cart_count() == 3


def test_remove_item_from_inventory_page(logged_in_page):
    inventory = InventoryPage(logged_in_page)
    inventory.add_to_cart(BACKPACK)
    inventory.add_to_cart(BIKE_LIGHT)

    inventory.remove_from_cart(BACKPACK)

    assert inventory.get_cart_count() == 1
    expect(inventory.product_button(BACKPACK)).to_have_text("Add to cart")


def test_cart_page_shows_added_items(logged_in_page):
    inventory = InventoryPage(logged_in_page)
    inventory.add_to_cart(BACKPACK)
    inventory.add_to_cart(BOLT_SHIRT)
    inventory.open_cart()

    cart = CartPage(logged_in_page)
    expect(logged_in_page).to_have_url("https://www.saucedemo.com/cart.html")
    assert cart.get_title() == "Your Cart"
    assert sorted(cart.get_item_names()) == sorted([BACKPACK, BOLT_SHIRT])


def test_remove_item_from_cart_page(logged_in_page):
    inventory = InventoryPage(logged_in_page)
    inventory.add_to_cart(BACKPACK)
    inventory.add_to_cart(BIKE_LIGHT)
    inventory.open_cart()

    cart = CartPage(logged_in_page)
    cart.remove_item(BACKPACK)

    assert cart.get_item_names() == [BIKE_LIGHT]
    assert inventory.get_cart_count() == 1


def test_continue_shopping_returns_to_inventory(logged_in_page):
    inventory = InventoryPage(logged_in_page)
    inventory.open_cart()

    CartPage(logged_in_page).continue_shopping()

    expect(logged_in_page).to_have_url("https://www.saucedemo.com/inventory.html")