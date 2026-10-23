from playwright.sync_api import expect

def test_saucedemo_login_page_loads(page):

    page.goto(
        "https://www.saucedemo.com/",
        wait_until="domcontentloaded",
        timeout=60000
    )

    expect(page.locator("#user-name")).to_be_visible()
    expect(page.locator("#password")).to_be_visible()
    expect(page.locator("#login-button")).to_be_visible()