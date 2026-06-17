import re

import allure
import pytest
from playwright.sync_api import Page, expect


def test_wikipedia_loads(wiki_page: Page):
    expect(wiki_page).to_have_title("Wikipedia")


# def test_login(page: Page, valid_user: dict[str, str]):
# page.goto("/login")

# page.get_by_label("Email").fill(valid_user["email"])
# page.get_by_label("Password").fill(valid_user["password"])
# page.get_by_role("button", name="Login").click()


def test_two_pages(browser):
    # browser fixture gives us the Browser object
    context = browser.new_context()
    page1 = context.new_page()
    page2 = context.new_page()

    page1.goto("https://www.wikipedia.org")
    page2.goto("https://books.toscrape.com")

    print(f"\nPage 1 title: {page1.title()}")
    print(f"Page 2 title: {page2.title()}")

    context.close()


@pytest.mark.parametrize(
    "search_value",
    [
        "Python",
        "Playwright",
        "Pytest",
    ],
)
@pytest.mark.smoke
@pytest.mark.ui
def test_wikipedia_locators(wiki_page: Page, search_value: str):
    # find the search box by its placeholder text
    search = wiki_page.get_by_placeholder("Search Wikipedia")
    print(f"\nSearch input visible: {search.is_visible()}")

    # find the English link by role + name
    english_link = wiki_page.get_by_role("link", name="English")
    print(f"English link text: {english_link.text_content()}")
    print(type(english_link))

    search_placeholder = wiki_page.get_by_role("searchbox")
    print(type(search_placeholder))
    search_placeholder.fill(search_value)
    search_placeholder.press("Enter")
    search_placeholder = wiki_page.locator("#searchInput")
    print(type(search_placeholder))
    search_placeholder.fill("searchInput")
    print(f"Filled search with: {search_value}")


def test_wikipedia_search(wiki_page: Page):
    # fill the search box and submit
    wiki_page.locator("#searchInput").fill("Python programming language")
    wiki_page.locator("#searchInput").press("Enter")

    # wait for the result page and check the heading
    expect(
        wiki_page.get_by_role("heading", name="Python (programming language)")
    ).to_be_visible()
    print(f"\nLanded on: {wiki_page.title()}")


def test_books_site_assertions(page: Page):
    page.goto("https://books.toscrape.com")

    # check page title contains "Books"
    expect(page).to_have_title(re.compile("Books"))

    # check there are book articles on the page
    books = page.get_by_role("article")
    expect(books).to_have_count(20)  # the site shows 20 books per page

    # check the first book has a rating attribute
    first_book = page.get_by_role("article").first
    expect(first_book).to_be_visible()

    print(f"\nBooks on page: {books.count()}")


@allure.title("Verify that the Travel category contains books")
@allure.description(
    """
    Navigate to the Books to Scrape website, open the Travel category,
    verify that the correct category page is displayed, and confirm
    that at least one book is available.
    """
)
def test_travel_category_has_books(page: Page):
    with allure.step("Open the Books to Scrape website"):
        page.goto("https://books.toscrape.com")

    with allure.step("Navigate to the Travel category"):
        page.get_by_role("link", name="Travel", exact=True).click()

    with allure.step("Verify that the Travel category page is displayed"):
        expect(page).to_have_url(re.compile(r"/travel_\d+/index\.html$"))

    with allure.step("Verify that the Travel category contains at least one book"):
        books = page.locator("article.product_pod")

        expect(
            books.first,
            "The Travel category should contain at least one book",
        ).to_be_visible()

        book_count = books.count()

        allure.attach(
            str(book_count),
            name="Number of books in the Travel category",
            attachment_type=allure.attachment_type.TEXT,
        )


@allure.title("Verify that a book detail page displays correct information")
@allure.description(
    """ 
    Open the Travel category, select the first available book, 
    and verify that its detail page displays the correct title, 
    price, and availability status. 
    """
)
def test_book_detail_page(page: Page):
    with allure.step("Open the Travel category page"):
        page.goto(
            "https://books.toscrape.com/catalogue/category/books/travel_2/index.html"
        )

    with allure.step("Get the first book title"):
        first_book = page.get_by_role("article").first
        first_book_link = first_book.locator("h3 a")
        first_book_title = (
            first_book_link.get_attribute("title") or first_book_link.inner_text()
        )

        allure.attach(
            first_book_title,
            name="Selected book",
            attachment_type=allure.attachment_type.TEXT,
        )

    with allure.step(f"Open the book detail page: {first_book_title}"):
        first_book_link.click()

    with allure.step("Verify that the correct book detail page is displayed"):
        book_heading = page.get_by_role("heading", level=1)
        expect(
            book_heading,
            f"The book detail page should display the title '{first_book_title}'",
        ).to_have_text(first_book_title)

    with allure.step("Verify that the book price is displayed in pounds"):
        price = page.locator(".product_main .price_color")
        expect(
            price,
            "The book price should be displayed in pounds",
        ).to_have_text(re.compile(r"^£\d+\.\d{2}$"))

        allure.attach(
            price.inner_text(),
            name="Book price",
            attachment_type=allure.attachment_type.TEXT,
        )

    with allure.step("Verify that the book is in stock"):
        availability = page.locator(".product_main .availability")
        expect(
            availability,
            "The book should be marked as in stock",
        ).to_contain_text("In stock")


@allure.title("Verify that a book can be added to the basket")
@allure.description(
    """
    Open the Mystery category, select the first available book,
    add it to the basket, and verify that a confirmation message
    is displayed.
    """
)
def test_add_to_basket(page: Page):
    with allure.step(
        "Open the https://books.toscrape.com/catalogue/category/books/mystery_3/index.html"
    ):
        page.goto(
            "https://books.toscrape.com/catalogue/category/books/mystery_3/index.html"
        )

    with allure.step("Open the first book detail page"):
        first_book = page.get_by_role("article").first
        first_book.get_by_role("link").first.click()

    # with allure.step("Add the book to the basket"):
    #     page.get_by_role("button", name="Add to basket").click()

    # with allure.step("# After adding, an alert/message should appear confirming it was added"):
    #     expect(page.get_by_role("alert")).to_be_visible()
    #     alert_text = page.get_by_role("alert").text_content()
    #     assert "basket" in alert_text.lower(), (f"Expected basket confirmation, got: {alert_text}")
    # print(f"\nBasket confirmation: {alert_text[:80]}")

    # alert = page.locator(".alert-success")

    # expect(
    #     alert,
    #     "A confirmation message should appear after adding a book to the basket",
    # ).to_be_visible()
    # allure.attach(
    #         alert.inner_text(),
    #         name="Add to basket confirmation",
    #         attachment_type=allure.attachment_type.TEXT,
    # )
