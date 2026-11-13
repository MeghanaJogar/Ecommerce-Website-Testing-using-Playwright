
from playwright.sync_api import sync_playwright, expect

URL = "https://www.saucedemo.com/"
USERNAME = "standard_user"
PASSWORD = "secret_sauce"


def test_sort_products_by_price():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            # Step 1: Open SauceDemo
            page.goto(URL)
            print("PASS: Website opened")

            # Step 2: Log in
            page.locator("#user-name").fill(USERNAME)
            page.locator("#password").fill(PASSWORD)
            page.locator("#login-button").click()

            expect(page.locator(".inventory_list")).to_be_visible()
            print("PASS: Login successful")

            # Step 3: Select Price (low to high)
            page.locator(".product_sort_container").select_option("lohi")
            print("PASS: Selected price low to high")

            # Step 4: Read the displayed product prices
            price_elements = page.locator(".inventory_item_price")
            prices = []

            for i in range(price_elements.count()):
                price_text = price_elements.nth(i).inner_text()
                prices.append(float(price_text.replace("$", "")))

            print("Displayed prices:", prices)

            # Step 5: Verify prices are in ascending order
            expect(page.locator(".inventory_item_price")).to_have_count(6)

            assert prices == sorted(prices), (
                f"Prices are not in ascending order: {prices}"
            )

            print("PASS: Products sorted from lowest to highest price")
            print("SORT PRODUCTS TEST PASSED")

        except Exception as error:
            print("TEST FAILED:", error)
            page.screenshot(
                path="sort_products_failure.png",
                full_page=True
            )
            raise

        finally:
            browser.close()


if __name__ == "__main__":
    test_sort_products_by_price()
