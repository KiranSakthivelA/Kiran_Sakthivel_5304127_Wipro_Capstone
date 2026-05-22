import pytest
import allure
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from pages.loginpage import LoginPage
from pages.labtestspage import LabTestsPage
from utils.csv_reader import get_csv_data
from utils.excel_reader import get_excel_data
from utils.screenshot_util import capture_screenshot
from utils.config_reader import get_config


@allure.epic("Apollo 247")
@allure.feature("Lab Tests Checkout Flow")
@pytest.mark.usefixtures("setup")
class TestLabTests:

    @allure.story("Lab Tests End-to-End")
    @allure.title("TC_02 - End to End Lab Test Booking (Parametrized)")
    def test_e2e_lab_tests(self, setup):
        driver = setup
        login_page = LoginPage(driver)
        lab_page   = LabTestsPage(driver)

        # ── Load parametrized data ────────────────────────────────────────────
        base_url     = get_config("Environment", "base_url")
        login_data   = get_csv_data("login_data.csv")[0]
        test_data    = get_csv_data("product_validation_data.csv")[0]
        patient_data = get_excel_data("test_data.xlsx")[0]
        payment_data = get_csv_data("payment_data.csv")[0]

        mobile_no    = login_data["mobile_number"]
        filter1      = test_data["filter1"]       # Top Deals
        filter2      = test_data["filter2"]       # Men's Health
        package_name = test_data["package_name"]  # Apollo Full Body Checkup
        
        card_name    = payment_data["card_name"]
        card_number  = payment_data["card_number"]
        exp_date     = payment_data["exp_date"]
        cvv          = payment_data["cvv"]

        # ── Step 1: Open Homepage ─────────────────────────────────────────────
        with allure.step("Step 1: Open Apollo 247 Homepage"):
            driver.get(base_url)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            login_page.dismiss_popups()
            capture_screenshot(driver, "01_homepage")
            assert "apollo" in driver.current_url.lower(), "Failed to load Apollo homepage"

        # ── Step 2: Login immediately ─────────────────────────────────────────
        with allure.step(f"Step 2: Login with mobile number {mobile_no}"):
            login_page.click_login_icon()
            login_page.dismiss_popups()
            login_page.enter_mobile_number(mobile_no)
            capture_screenshot(driver, "02_mobile_entered")
            login_page.click_continue()          # clicks "Continue" button
            capture_screenshot(driver, "03_otp_screen")

        # ── Step 3: Wait 15 sec for manual OTP ───────────────────────────────
        with allure.step("Step 3: Waiting 15 seconds for manual OTP entry"):
            login_page.wait_for_otp_entry(wait_seconds=15)
            login_page.dismiss_popups()
            capture_screenshot(driver, "04_after_login")

        # ── Step 4: Navigate to Lab Tests ────────────────────────────────────
        with allure.step("Step 4: Navigate to Lab Tests > Popular Health Checkup Packages"):
            lab_page.go_to_lab_tests()
            capture_screenshot(driver, "05_lab_tests_page")
            assert "lab-tests" in driver.current_url.lower() or "diagnostics" in driver.current_url.lower(), "Failed to navigate to Lab Tests"
            lab_page.click_popular_view_all()
            capture_screenshot(driver, "06_popular_packages_listing")
            assert "popular-health-checkup" in driver.current_url.lower(), "Failed to load popular checkups"

        # ── Step 5: Apply Filters & Sort ──────────────────────────────────────
        with allure.step(f"Step 5: Apply filters '{filter1}' and '{filter2}' and Sort"):
            lab_page.apply_filter(filter1)
            capture_screenshot(driver, "07_filter_top_deals")
            lab_page.apply_filter(filter2)
            capture_screenshot(driver, "08_filter_mens_health")
            lab_page.sort_low_to_high()
            capture_screenshot(driver, "08_sort_low_to_high")

        # ── Step 6: Add package to cart ───────────────────────────────────────
        with allure.step(f"Step 6: Add '{package_name}' to cart"):
            lab_page.add_package_to_cart(package_name)
            capture_screenshot(driver, "09_package_added")
            lab_page.proceed_to_cart_popup()
            capture_screenshot(driver, "10_cart_popup")

        # ── Step 7: Select Patient ───────────────────────────────────────────
        with allure.step("Step 7: Select Patient 'Test User'"):
            lab_page.select_patient("Test User")
            capture_screenshot(driver, "11_patient_selected")

        # ── Step 8: Select Address ───────────────────────────────────────────
        with allure.step("Step 8: Select Address 7A"):
            lab_page.select_address("7A")
            capture_screenshot(driver, "12_address_selected")

        # ── Step 9: Select Schedule ───────────────────────────────────────────
        with allure.step("Step 9: Select Schedule 22 May 2026 06:30 AM - 07:30 AM"):
            lab_page.select_schedule("22 May 2026", "06:30 AM")
            capture_screenshot(driver, "13_schedule_selected")

        # ── Step 10: Proceed to Pay ───────────────────────────
        with allure.step("Step 10: Proceed to Pay"):
            lab_page.proceed_to_pay()
            capture_screenshot(driver, "14_proceed_to_pay")
            
        time.sleep(2)
        assert "checkout" in driver.current_url.lower() or "payment" in driver.current_url.lower() or "cart" in driver.current_url.lower(), "Failed to reach checkout/payment page"
        
        # ── Attach Full Execution Log at the bottom ───────────────────────────
        with allure.step("Execution Logs"):
            import os
            log_path = os.path.join(os.path.dirname(__file__), "..", "logs", "automation.log")
            if os.path.exists(log_path):
                with open(log_path, "r", encoding="utf-8", errors="replace") as f:
                    allure.attach(f.read(), name="Full Execution Log", attachment_type=allure.attachment_type.TEXT)

        assert True, "E2E Lab Test Booking flow completed successfully"
