import base64
import re
from pathlib import Path

import pytest
from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
from utils.config import (
    BASE_URL, HEADLESS, SLOW_MO, DEFAULT_TIMEOUT, DEMO_PAUSE,
    STANDARD_USER, PASSWORD,
)

REPORTS_DIR = Path(__file__).resolve().parent / "reports"
SCREENSHOTS_DIR = REPORTS_DIR / "screenshots"
TRACES_DIR = REPORTS_DIR / "traces"


def safe_name(name):
    return re.sub(r"[^\w\-]", "_", name)


# ---------- Hook: har test ka result save karo + fail pe screenshot ----------
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page is None:
            return

        SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
        path = SCREENSHOTS_DIR / f"{safe_name(item.name)}.png"
        image_bytes = page.screenshot(path=str(path), full_page=True)

        # Screenshot ko HTML report ke andar embed karo
        html_plugin = item.config.pluginmanager.getplugin("html")
        if html_plugin:
            extras = getattr(report, "extras", [])
            extras.append(html_plugin.extras.png(base64.b64encode(image_bytes).decode()))
            report.extras = extras


# ---------- Fixtures ----------
@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS, slow_mo=SLOW_MO)
        yield browser
        browser.close()


@pytest.fixture
def page(browser, request):
    context = browser.new_context(viewport={"width": 1366, "height": 768})
    context.tracing.start(screenshots=True, snapshots=True, sources=True)

    page = context.new_page()
    page.set_default_timeout(DEFAULT_TIMEOUT)
    page.goto(BASE_URL)
    yield page

    page.wait_for_timeout(DEMO_PAUSE)

    # Trace sirf fail hone pe save karo
    rep = getattr(request.node, "rep_call", None)
    if rep is not None and rep.failed:
        TRACES_DIR.mkdir(parents=True, exist_ok=True)
        context.tracing.stop(path=str(TRACES_DIR / f"{safe_name(request.node.name)}.zip"))
    else:
        context.tracing.stop()

    context.close()


@pytest.fixture
def logged_in_page(page):
    page.goto(BASE_URL)
    LoginPage(page).login(STANDARD_USER, PASSWORD)
    page.wait_for_url("**/inventory.html")
    return page