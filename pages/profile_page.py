# pages/profile_page.py

from urllib.parse import urljoin

from playwright.sync_api import Locator, Page

from components.toast import Toast
from models.profile_data import ProfileData


class ProfilePage:
    PATH = "/wiki"

    def __init__(self, page: Page, base_url: str) -> None:
        self._page = page
        self._url = urljoin(base_url.rstrip("/") + "/", self.PATH.lstrip("/"))

        self.name_input: Locator = page.get_by_label("Name")
        self.save_button: Locator = page.get_by_role(
            "button",
            name="Save",
            exact=True,
        )

        self.toast = Toast(page)

    def open(self) -> None:
        self._page.goto(self._url)

    def clear_name(self) -> None:
        self.name_input.clear()

    def enter_name(self, name: str) -> None:
        self.name_input.fill(name)

    def fill_profile(self, profile: ProfileData) -> None:
        self.enter_name(profile.name)

    def save(self) -> None:
        self.save_button.click()
