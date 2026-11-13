from playwright.sync_api import sync_playwright, expect
 
# ==========================================
# TEST DATA
# ==========================================
 
URL = "https://www.saucedemo.com/"
 
USERNAME = "standard_user"
PASSWORD = "secret_sauce"
 
PRODUCTS = [
    "Sauce Labs Backpack",
    "Sauce Labs Bike Light"
]
 
ADDITIONAL_PRODUCTS = [
    "Sauce Labs Bolt T-Shirt",
    "Sauce Labs Fleece Jacket"
]
 
 
# ==========================================
# LOGIN
# ==========================================
 
def login(page):
    print("Opening application...")
 
    page.goto(URL)
 
    page.locator("#user-name").fill(USERNAME)
    page.locator("#password").fill(PASSWORD)
 
    page.locator("#login-button").click()
 
    expect(page.locator(".inventory_list")).to_be_visible()
 
    print("Login successful")
 
 
# ==========================================
# ADD PRODUCTS TO CART
# ==========================================
 
def add_product(page, product_name):
 
    product = page.locator(".inventory_item").filter(
        has=page.locator(
            ".inventory_item_name",
            has_text=product_name
        )
    )
 
    product.locator("button", has_text="Add to cart").click()
 
    print(f"Added to cart: {product_name}")
 
 
# ==========================================
# ADD INITIAL PRODUCTS
# ==========================================
 
def add_initial_products(page):
 
    for product in PRODUCTS:
        add_product(page, product)
 
 
# ==========================================
# FIND AND ADD ADDITIONAL PRODUCTS
# ==========================================
 
def search_and_add_products(page):
 
    print("Finding additional products...")
 
    # SauceDemo does not provide a search bar.
    # Find products by their displayed names.
 
    for product in ADDITIONAL_PRODUCTS:
        add_product(page, product)
 
 
# ==========================================
# VERIFY CART
# ==========================================
 
def verify_cart(page):
 
    page.locator(".shopping_cart_link").click()
 
    expect(page).to_have_url("https://www.saucedemo.com/cart.html")
 
    cart_items = page.locator(".cart_item")
 
    expected_count = len(PRODUCTS) + len(ADDITIONAL_PRODUCTS)
 
    expect(cart_items).to_have_count(expected_count)
 
    print(f"Cart verified: {expected_count} products")
 
 
# ==========================================
# CHECKOUT
# ==========================================
 
def checkout(page):
 
    page.locator("#checkout").click()
 
    print("Checkout started")
 
    page.locator("#first-name").fill("Test")
    page.locator("#last-name").fill("User")
    page.locator("#postal-code").fill("411001")
 
    page.locator("#continue").click()
 
    expect(page.locator(".summary_info")).to_be_visible()
 
    print("Checkout overview reached")
    print("No order placed and no payment made")
 
    # IMPORTANT:
    # Do NOT click #finish.
    # This would complete the demo order.
 
 
# ==========================================
# LOGOUT
# ==========================================
 
def logout(page):
 
    page.locator("#react-burger-menu-btn").click()
 
    page.locator("#logout_sidebar_link").click()
 
    expect(page.locator("#login-button")).to_be_visible()
 
    print("Logout successful")
 
 
# ==========================================
# MAIN AUTOMATION
# ==========================================
 
def run_test():
 
    with sync_playwright() as playwright:
 
        browser = playwright.chromium.launch(
            headless=False,
            slow_mo=500
        )
 
        page = browser.new_page()
 
        try:
            login(page)
 
            add_initial_products(page)
 
            search_and_add_products(page)
 
            verify_cart(page)
 
            checkout(page)
 
            page.wait_for_timeout(2000)
 
            logout(page)
 
            print("\nEND-TO-END TEST PASSED")
 
        except Exception as error:
 
            print("\nTEST FAILED:", error)
 
            page.screenshot(
                path="error_screenshot.png",
                full_page=True
            )
 
            raise
 
        finally:
            browser.close()
 
 
# ==========================================
# EXECUTION
# ==========================================
 
if __name__ == "__main__":
    run_test()