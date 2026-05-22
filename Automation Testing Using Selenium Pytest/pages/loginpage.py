import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.basepage import BasePage

class LoginPage(BasePage):
    # Locators
    LOGIN_ICON  = (By.XPATH, "//span[contains(@class,'icon-ic_account')] | //button[contains(text(),'Sign In')] | //span[contains(text(),'Sign In')]")
    MOBILE_INPUT = (By.XPATH, "//input[@type='tel'] | //input[@name='mobileNumber'] | //input[@placeholder='Enter Mobile Number']")
    CONTINUE_BTN = (By.XPATH, "//button[normalize-space(text())='Continue']")
    OTP_SCREEN   = (By.XPATH, "//div[contains(text(),'Enter OTP') or contains(text(),'OTP')]")

    def click_login_icon(self):
        self.logger.info("Clicking login/sign-in icon immediately via JS")
        # Removing all explicit waits here to fix the latency issue
        self.driver.execute_script("""
            let el = document.querySelector('[class*="userCircle"], [class*="login"], [class*="signIn"], [class*="account"], [class*="icon-ic_account"]');
            if (el) el.click();
            else {
                let btns = Array.from(document.querySelectorAll('button, span, a'));
                let loginBtn = btns.find(b => (b.textContent || '').toLowerCase().includes('login') || (b.textContent || '').toLowerCase().includes('sign in'));
                if (loginBtn) loginBtn.click();
            }
        """)

    def enter_mobile_number(self, mobile_no):
        self.logger.info(f"Entering mobile number: {mobile_no}")
        try:
            self.wait.until(EC.presence_of_element_located(self.MOBILE_INPUT))
            field = self.driver.find_element(*self.MOBILE_INPUT)
            field.clear()
            field.send_keys(mobile_no)
        except Exception as e:
            self.logger.warning(f"Mobile input issue: {e}")

    def click_continue(self):
        """Click the Continue button after entering mobile number."""
        self.logger.info("Clicking Continue button")
        try:
            self.click_element(self.CONTINUE_BTN)
        except Exception:
            self.driver.execute_script("""
                let b = Array.from(document.querySelectorAll('button'))
                             .find(el => el.textContent.trim() === 'Continue');
                if (b) b.click();
            """)
        self.logger.info("Continue clicked. Waiting 15 seconds for manual OTP entry...")

    def wait_for_otp_entry(self, wait_seconds=15):
        """Wait for user to manually enter OTP."""
        self.logger.info(f"Waiting {wait_seconds} seconds for manual OTP entry...")
        time.sleep(wait_seconds)
        self.logger.info("OTP wait complete. Proceeding to next step.")

    # keep backward compat alias used in test files
    def submit_login(self):
        self.click_continue()

    def wait_for_otp_and_login(self):
        self.wait_for_otp_entry(wait_seconds=15)
