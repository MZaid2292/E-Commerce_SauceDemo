import json
from pathlib import Path

import pytest
from pages.login_page import LoginPage

DATA_FILE = (
    Path(__file__).resolve().parents[1]
    / "test_data"
    / "login_data.json"
)

with DATA_FILE.open("r", encoding="utf-8") as file:
    LOGIN_TEST_DATA = json.load(file)

@pytest.mark.login
@pytest.mark.parametrize(
    "case",
    LOGIN_TEST_DATA,
    ids=[case["test_id"] for case in LOGIN_TEST_DATA]
)

def test_login_scenarios(page,case):
    login_page = LoginPage(page)

    login_page.open_login_page()
    login_page.login(
        case["username"],
        case["password"]
    )

    if case["expected"] == "success":
        assert login_page.is_products_page_visible(), (
            "Successful login should display the products page."
        )
    else:
        actual_message = login_page.get_error_message()

        assert case["expected"] in actual_message, (
            f"Expected error: {case["expected"]}. "
            f"Actual error: {actual_message}"
        )    