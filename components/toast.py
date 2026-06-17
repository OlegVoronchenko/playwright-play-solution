# components/toast.py

from playwright.sync_api import Locator, Page


class Toast:

    def __init__(self, page: Page) -> None:
        self._root: Locator = page.get_by_role("status")

    @property
    def root(self) -> Locator:
        return self._root