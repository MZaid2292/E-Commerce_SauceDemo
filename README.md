# SauceDemo E-Commerce QA Automation Framework

End-to-end UI test automation framework for the [SauceDemo](https://www.saucedemo.com) e-commerce website, built with **Python, Playwright and Pytest** using a Hybrid Framework approach (Page Object Model + Data-Driven Testing).

## Tech Stack

| Tool | Purpose |
|---|---|
| Python 3 | Programming language |
| Playwright | Browser automation |
| Pytest | Test runner, fixtures, markers, parametrization |
| pytest-html | HTML test report |
| JSON | External test data |

## Framework Features

- **Page Object Model (POM)** with a reusable `BasePage` wrapper
- **Data-driven testing** with JSON files (login and checkout validation)
- **Pytest fixtures** for browser setup, teardown and pre-logged-in sessions
- **Markers** to run test groups (smoke, regression, login, inventory, cart, checkout)
- **Parametrized tests** with readable test IDs
- **Auto screenshot on failure**, embedded in the HTML report
- **Playwright trace** saved on failure for step-by-step debugging
- **Logging** of page actions to a log file

## Project Structure

```
├── pages/                  # Page Object classes
│   ├── base_page.py        # Common actions (click, fill, logout)
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── cart_page.py
│   └── checkout_page.py
├── tests/                  # Test cases
│   ├── test_smoke.py
│   ├── test_login.py
│   ├── test_inventory.py
│   ├── test_cart.py
│   ├── test_checkout.py
│   └── test_logout.py
├── test_data/              # JSON test data
├── utils/                  # Config and data loader
├── docs/                   # Test plan and test cases
├── conftest.py             # Fixtures and reporting hooks
├── pytest.ini              # Pytest configuration and markers
└── requirements.txt
```

## Test Coverage (27 tests)

| Module | Scenarios |
|---|---|
| Smoke | Login page loads |
| Login | Valid login, invalid username/password, empty credentials |
| Inventory | Page loads, 6 products shown, name and price present, sort by name (A-Z, Z-A), sort by price (low-high, high-low) |
| Cart | Empty cart, add single/multiple items, remove from inventory and cart page, continue shopping |
| Checkout | Missing first name / last name / postal code validation, overview total calculation, complete order end-to-end, cancel checkout |
| Logout | Logout redirects to login, inventory blocked after logout |

## Setup

```bash
git clone https://github.com/MZaid2292/saucedemo-qa-automation.git
cd saucedemo-qa-automation

python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux / Mac
source .venv/bin/activate

pip install -r requirements.txt
playwright install chromium
```

## Running Tests

```bash
pytest                    # run all tests
pytest -m smoke           # smoke tests only
pytest -m checkout        # one module
pytest tests/test_cart.py # one file
```

## Reports

After a run, the `reports/` folder contains:

- `report.html` – HTML report (failed tests include a screenshot)
- `test_run.log` – action log
- `screenshots/` – screenshots of failed tests
- `traces/` – Playwright traces of failed tests

Open a trace:
```bash
playwright show-trace reports/traces/<test_name>.zip
```

## Documentation

Manual QA artifacts are in the `docs/` folder:
- `test_plan.md`
- `test_cases.md`

 
