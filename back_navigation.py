
from playwright.sync_api import sync_playwright, expect

URL = "https://www.saucedemo.com/"
USERNAME = "standard_user"
PASSWORD = "secret_sauce"


def test_back_navigation():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            # Step 1: Login
            page.goto(URL)
            page.locator("#user-name").fill(USERNAME)
            page.locator("#password").fill(PASSWORD)
            page.locator("#login-button").click()

            expect(page.locator(".inventory_list")).to_be_visible()
            print("PASS: Login successful")

            # Step 2: Add a product
            backpack = page.locator(".inventory_item").filter(
                has=page.get_by_text(
                    "Sauce Labs Backpack", exact=True
                )
            )
            backpack.get_by_role(
                "button", name="Add to cart"
            ).click()

            expect(page.locator(".shopping_cart_badge")).to_have_text("1")
            print("PASS: Product added to cart")

            # Step 3: Open cart
            page.locator(".shopping_cart_link").click()
            expect(page).to_have_url(
                "https://www.saucedemo.com/cart.html"
            )
            expect(page.locator(".cart_item")).to_have_count(1)
            print("PASS: Cart contains one product")

            # Step 4: Navigate backward
            page.go_back()

            expect(page.locator(".inventory_list")).to_be_visible()
            print("PASS: Back navigation returned to products")

            # Step 5: Verify cart still has one product
            expect(page.locator(".shopping_cart_badge")).to_have_text("1")
            print("PASS: Cart badge still shows one product")

            # Step 6: Open cart again and verify
            page.locator(".shopping_cart_link").click()
            expect(page.locator(".cart_item")).to_have_count(1)
            print("PASS: Product remains in cart")

            print("BACK NAVIGATION TEST PASSED")

        except Exception as error:
            print("TEST FAILED:", error)
            page.screenshot(
                path="back_navigation_failure.png",
                full_page=True
            )
            raise

        finally:
            browser.close()


if __name__ == "__main__":
    test_back_navigation()
