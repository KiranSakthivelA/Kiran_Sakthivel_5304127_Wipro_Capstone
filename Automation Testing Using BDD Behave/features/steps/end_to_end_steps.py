import time
from behave import given, when, then
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from pages.loginpage import LoginPage
from pages.labtestspage import LabTestsPage
from utils.csv_reader import get_csv_data
from utils.screenshot_util import capture_screenshot
from utils.config_reader import get_config

@given('I open Apollo 247 Homepage')
def step_impl(context):
    context.login_page = LoginPage(context.driver)
    context.lab_page = LabTestsPage(context.driver)
    
    base_url = get_config("Environment", "base_url")
    context.driver.get(base_url)
    WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    context.login_page.dismiss_popups()
    capture_screenshot(context.driver, "01_homepage")
    assert "apollo" in context.driver.current_url.lower(), "Failed to load Apollo homepage"

@when('I login with my mobile number')
def step_impl(context):
    login_data = get_csv_data("login_data.csv")[0]
    mobile_no = login_data["mobile_number"]
    
    context.login_page.click_login_icon()
    context.login_page.dismiss_popups()
    context.login_page.enter_mobile_number(mobile_no)
    capture_screenshot(context.driver, "02_mobile_entered")
    context.login_page.click_continue()
    capture_screenshot(context.driver, "03_otp_screen")

@when('I wait for manual OTP entry')
def step_impl(context):
    context.login_page.wait_for_otp_entry(wait_seconds=15)
    context.login_page.dismiss_popups()
    capture_screenshot(context.driver, "04_after_login")

@when('I navigate to Lab Tests Popular Health Checkup Packages')
def step_impl(context):
    context.lab_page.go_to_lab_tests()
    capture_screenshot(context.driver, "05_lab_tests_page")
    assert "lab-tests" in context.driver.current_url.lower() or "diagnostics" in context.driver.current_url.lower(), "Failed to navigate to Lab Tests"
    
    context.lab_page.click_popular_view_all()
    capture_screenshot(context.driver, "06_popular_packages_listing")
    assert "popular-health-checkup" in context.driver.current_url.lower(), "Failed to load popular checkups"

@when('I apply filters "{filter1}" and "{filter2}" and Sort Low to High')
def step_impl(context, filter1, filter2):
    context.lab_page.apply_filter(filter1)
    capture_screenshot(context.driver, "07_filter_top_deals")
    
    context.lab_page.apply_filter(filter2)
    capture_screenshot(context.driver, "08_filter_mens_health")
    
    context.lab_page.sort_low_to_high()
    capture_screenshot(context.driver, "08_sort_low_to_high")

@when('I add package "{package_name}" to cart')
def step_impl(context, package_name):
    context.lab_page.add_package_to_cart(package_name)
    capture_screenshot(context.driver, "09_package_added")
    
    context.lab_page.proceed_to_cart_popup()
    capture_screenshot(context.driver, "10_cart_popup")

@when('I select Patient "{patient_name}"')
def step_impl(context, patient_name):
    context.lab_page.select_patient(patient_name)
    capture_screenshot(context.driver, "11_patient_selected")

@when('I select Address "{address}"')
def step_impl(context, address):
    context.lab_page.select_address(address)
    capture_screenshot(context.driver, "12_address_selected")

@when('I select Schedule "{schedule_date}" at "{schedule_time}"')
def step_impl(context, schedule_date, schedule_time):
    context.lab_page.select_schedule(schedule_date, schedule_time)
    capture_screenshot(context.driver, "13_schedule_selected")

@when('I proceed to pay')
def step_impl(context):
    context.lab_page.proceed_to_pay()
    capture_screenshot(context.driver, "14_proceed_to_pay")
    time.sleep(2)

@then('I should be on the checkout page')
def step_impl(context):
    assert "checkout" in context.driver.current_url.lower() or "payment" in context.driver.current_url.lower() or "cart" in context.driver.current_url.lower(), "Failed to reach checkout/payment page"
