import os

import pytest
from playwright.sync_api import Page, expect
from pytest_playwright import CreateContextCallback


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {
            "width": 1440,
            "height": 900,
        },
        "locale": "en-US",
        "timezone_id": "Europe/Lisbon",
    }


@pytest.fixture
def wiki_page(page: Page) -> Page:
    page.goto("/")
    return page


@pytest.fixture
def authenticated_page(
    new_context: CreateContextCallback,
) -> Page:
    context = new_context(storage_state="test-data/auth-state.json")

    page = context.new_page()
    return page


@pytest.fixture
def valid_user() -> dict[str, str]:
    return {
        "email": "test@example.com",
        "password": "Password123!",
    }


# conftest.py

expect.set_options(timeout=5_000)


@pytest.fixture(scope="session")
def base_url() -> str:
    return os.getenv("APP_URL", "https://www.wikipedia.org")


@pytest.fixture
def configured_page(page: Page) -> Page:
    # click(), fill(), goto() etc.
    page.set_default_timeout(10_000)
    page.set_default_navigation_timeout(30_000)
    return page
