
from playwright.sync_api import sync_playwright, expect

URL = "https://www.saucedemo.com/"


def test_invalid_login():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            # Step 1: Open SauceDemo
            page.goto(URL)
            print("PASS: SauceDemo website opened")

            # Step 2: Enter invalid login credentials
            page.locator("#user-name").fill("invalid_user")
            page.locator("#password").fill("wrong_password")

            # Step 3: Click Login
            page.locator("#login-button").click()
            print("PASS: Login button clicked")

            # Step 4: Verify the error message
            error_message = page.locator(
                "[data-test='error']"
            )
            expect(error_message).to_be_visible()

            print("PASS: Error message displayed")
            print("Error:", error_message.inner_text())

            # Step 5: Verify the user remains on the login page
            expect(page.locator("#login-button")).to_be_visible()
            expect(page.locator("#user-name")).to_be_visible()

            print("PASS: User was not logged in")
            print("INVALID LOGIN TEST PASSED")

        except Exception as error:
            print("TEST FAILED:", error)
            page.screenshot(
                path="invalid_login_failure.png",
                full_page=True
            )
            raise

        finally:
            browser.close()


if __name__ == "__main__":
    test_invalid_login()
