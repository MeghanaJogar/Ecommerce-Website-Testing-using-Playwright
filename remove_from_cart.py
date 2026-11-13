
from playwright.sync_api import sync_playwright, expect

URL = "https://www.saucedemo.com/"
USERNAME = "standard_user"
PASSWORD = "secret_sauce"


def test_remove_product_from_cart():
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

            # Step 3: Add the first product
            backpack = page.locator(".inventory_item").filter(
                has=page.get_by_text(
                    "Sauce Labs Backpack", exact=True
                )
            )
            backpack.get_by_role(
                "button", name="Add to cart"
            ).click()
            print("PASS: Backpack added to cart")

            # Step 4: Add the second product
            bike_light = page.locator(".inventory_item").filter(
                has=page.get_by_text(
                    "Sauce Labs Bike Light", exact=True
                )
            )
            bike_light.get_by_role(
                "button", name="Add to cart"
            ).click()
            print("PASS: Bike Light added to cart")

            # Step 5: Verify cart count is 2
            expect(
                page.locator(".shopping_cart_badge")
            ).to_have_text("2")
            print("PASS: Cart contains 2 products")

            # Step 6: Remove the Backpack
            backpack.get_by_role(
                "button", name="Remove"
            ).click()
            print("PASS: Backpack removed")

            # Step 7: Verify cart count is now 1
            expect(
                page.locator(".shopping_cart_badge")
            ).to_have_text("1")
            print("PASS: Cart count decreased to 1")

            # Step 8: Open cart and verify remaining product
            page.locator(".shopping_cart_link").click()

            expect(page.locator(".cart_item")).to_have_count(1)
            expect(
                page.locator(".cart_item")
            ).to_contain_text("Sauce Labs Bike Light")

            expect(
                page.get_by_text(
                    "Sauce Labs Backpack", exact=True
                )
            ).to_have_count(0)

            print("PASS: Only Bike Light remains in cart")
            print("REMOVE PRODUCT TEST PASSED")

        except Exception as error:
            print("TEST FAILED:", error)
            page.screenshot(
                path="remove_from_cart_failure.png",
                full_page=True
            )
            raise

        finally:
            browser.close()


if __name__ == "__main__":
    test_remove_product_from_cart()
