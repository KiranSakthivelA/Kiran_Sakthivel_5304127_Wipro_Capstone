import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utils.logger import LogGen

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)
        self.logger = LogGen.loggen()

    def wait_for_element(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def click_element(self, locator):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def enter_text(self, locator, text):
        element = self.wait_for_element(locator)
        element.clear()
        element.send_keys(text)

    def dismiss_popups(self):
        """Aggressively remove ALL overlays, banners, sticky bars, and modals via JS."""
        try:
            self.driver.execute_script("""
                // Remove CleverTap / WebEngage notification banners
                document.querySelectorAll('[class*="wzrk"], [id*="wzrk"], #wzrk-container').forEach(el => el.remove());

                // Remove bottom sticky bars (Circle upsell, Go To Cart bar, etc.)
                document.querySelectorAll('[class*="sticky"], [class*="Sticky"], [class*="bottomBar"], [class*="BottomBar"], [class*="bottom-bar"]')
                    .forEach(el => {
                        let txt = (el.textContent || '').toLowerCase();
                        if (txt.includes('upgrade') || txt.includes('circle') || txt.includes('go to cart') ||
                            txt.includes('need assistance') || txt.includes('callback') || txt.includes('call assistance'))
                            el.remove();
                    });

                // Generic text-based removal for any banner/div containing Need Assistance
                document.querySelectorAll('div, section, aside').forEach(el => {
                    let txt = (el.textContent || '').toLowerCase();
                    if (txt.includes('need assistance?') && txt.includes('request a callback')) {
                        // Only hide elements that look like banners (short height) to avoid hiding the entire page wrapper!
                        if (el.offsetHeight > 0 && el.offsetHeight < 150) {
                            el.style.display = 'none';
                        }
                    }
                });


                // Remove dialog/modal overlays that are not the login/OTP modal
                document.querySelectorAll('[role="dialog"], [class*="modal"], [class*="Modal"], [class*="dialog"], [class*="Dialog"]')
                    .forEach(el => {
                        let txt = (el.textContent || '').toLowerCase();
                        if (txt.includes('need help') || txt.includes('request a callback') ||
                            txt.includes('incomplete') || txt.includes('upgrade') || txt.includes('circle membership') ||
                            txt.includes('need assistance') || txt.includes('call assistance'))
                            el.remove();
                    });


                // Dismiss mega menu hover overlays
                document.querySelectorAll('[class*="megaMenu"], [class*="MegaMenu"]').forEach(el => el.remove());

                // Click "Continue Booking" if the resume modal is open
                let cb = Array.from(document.querySelectorAll('button, span, div')).find(el => {
                    let t = (el.textContent || '').trim().toLowerCase();
                    return t === 'continue booking' && el.offsetHeight > 0;
                });
                if (cb) { try { cb.click(); } catch(e) {} }

                // Remove backdrop overlays
                document.querySelectorAll('.modal-backdrop, [class*="backdrop"], [class*="Backdrop"]').forEach(el => el.remove());
            """)
            time.sleep(0.5)
        except Exception as e:
            self.logger.warning(f"Popup dismiss error: {e}")
