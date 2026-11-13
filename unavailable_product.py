
from playwright.sync_api import sync_playwright, expect

URL = "https://www.saucedemo.com/"
USERNAME = "standard_user"
PASSWORD = "secret_sauce"
UNAVAILABLE_PRODUCT = "XYZ Unavailable Product"


def test_unavailable_product():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            # Step 1: Open SauceDemo
            page.goto(URL)
            print("PASS: SauceDemo website opened")

            # Step 2: Log in
            page.locator("#user-name").fill(USERNAME)
            page.locator("#password").fill(PASSWORD)
            page.locator("#login-button").click()

            expect(page.locator(".inventory_list")).to_be_visible()
            print("PASS: Login successful")

            # Step 3: Verify the requested product does not exist
            product = page.locator(".inventory_item").filter(
                has=page.get_by_text(
                    UNAVAILABLE_PRODUCT, exact=True
                )
            )

            expect(product).to_have_count(0)
            print("PASS: Unavailable product was not found")

            # Step 4: Verify the cart is empty
            expect(
                page.locator(".shopping_cart_badge")
            ).to_have_count(0)

            print("PASS: Cart remains empty")
            print("UNAVAILABLE PRODUCT TEST PASSED")

        except Exception as error:
            print("TEST FAILED:", error)
            page.screenshot(
                path="unavailable_product_failure.png",
                full_page=True
            )
            raise

        finally:
            browser.close()


if __name__ == "__main__":
    test_unavailable_product()
