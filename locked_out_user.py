
from playwright.sync_api import sync_playwright, expect

URL = "https://www.saucedemo.com/"
USERNAME = "locked_out_user"
PASSWORD = "secret_sauce"


def test_locked_out_user():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            # Step 1: Open SauceDemo
            page.goto(URL)
            print("PASS: SauceDemo website opened")

            # Step 2: Enter locked-out user credentials
            page.locator("#user-name").fill(USERNAME)
            page.locator("#password").fill(PASSWORD)
            print("PASS: Login credentials entered")

            # Step 3: Click Login
            page.locator("#login-button").click()
            print("PASS: Login button clicked")

            # Step 4: Verify the error message
            error_message = page.locator("[data-test='error']")

            expect(error_message).to_be_visible()
            expect(error_message).to_contain_text(
                "Sorry, this user has been locked out"
            )

            print("PASS: Locked-out error message displayed")
            print("Error:", error_message.inner_text())

            # Step 5: Verify login did not succeed
            expect(page.locator("#login-button")).to_be_visible()
            expect(page.locator("#user-name")).to_be_visible()

            print("PASS: User remains on login page")
            print("LOCKED-OUT USER TEST PASSED")

        except Exception as error:
            print("TEST FAILED:", error)
            page.screenshot(
                path="locked_out_user_failure.png",
                full_page=True
            )
            raise

        finally:
            browser.close()


if __name__ == "__main__":
    test_locked_out_user()
