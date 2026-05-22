import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from pages.basepage import BasePage


class LabTestsPage(BasePage):
    # Locators
    LAB_TESTS_LINK   = (By.XPATH, "//a[normalize-space(text())='Lab Tests'] | //span[normalize-space(text())='Lab Tests']")
    POPULAR_VIEW_ALL = (By.XPATH, "//span[contains(text(),'View All') or contains(text(),'View all')]")
    SELECT_SLOT_BTN  = (By.XPATH, "//button[contains(text(),'Select Slot')]")
    PROCEED_PAY_BTN  = (By.XPATH, "//button[contains(text(),'Proceed to Pay')]")

    # ── Navigation ────────────────────────────────────────────────────────────

    def go_to_lab_tests(self):
        self.logger.info("Clicking 'Lab Tests' in header")
        try:
            self.click_element(self.LAB_TESTS_LINK)
        except Exception:
            self.driver.execute_script(
                "let a = Array.from(document.querySelectorAll('a, span'))"
                ".find(el => el.textContent.trim() === 'Lab Tests'); if(a) a.click();"
            )
        time.sleep(2)
        self.dismiss_popups()

    def click_popular_view_all(self):
        self.logger.info("Waiting for 'View All' on Popular Health Checkups")
        # We MUST use native Selenium clicks because JS clicks on React Router links
        # can cause full page reloads that crash the Apollo247 application.
        
        for _ in range(15):
            try:
                # 1. Find the View All link using Selenium
                xpath = "//a[contains(@href, 'popular-health-checkup')]"
                links = self.driver.find_elements(By.XPATH, xpath)
                
                if not links:
                    # Alternative XPath looking for View All text near the heading
                    xpath = "//*[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'popular health checkup packages')]/ancestor::div[1]//*[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'view all')]"
                    links = self.driver.find_elements(By.XPATH, xpath)
                
                if links:
                    # 2. Scroll exactly to the link so it's in the center of the screen
                    self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", links[0])
                    time.sleep(2)  # Wait for smooth scrolling to finish
                    
                    self.dismiss_popups()
                    time.sleep(1)
                    
                    # 3. Perform a real mouse click
                    ActionChains(self.driver).move_to_element(links[0]).click().perform()
                    self.logger.info("Successfully clicked 'View All' natively")
                    break
                    
            except Exception as e:
                self.logger.warning(f"Failed to click View All natively: {e}")
            time.sleep(1)
            
        time.sleep(3)
        self.dismiss_popups()

    # ── Filters ───────────────────────────────────────────────────────────────

    def apply_filter(self, filter_name):
        """Click a filter label (e.g. 'Top Deals', "Men's Health")."""
        self.logger.info(f"Applying filter: {filter_name}")
        try:
            time.sleep(2)  # Wait before selecting filter
            self.dismiss_popups()
            
            labels = self.driver.find_elements(By.TAG_NAME, "label")
            matched = [l for l in labels if filter_name.lower().strip() in (l.text or "").lower().strip()]
            if not matched:
                elements = self.driver.find_elements(By.XPATH, "//*[self::div or self::span or self::p or self::a]")
                matched = [el for el in elements if filter_name.lower().strip() in (el.text or "").lower().strip() and len((el.text or "").strip()) < 40]
            
            if matched:
                matched.sort(key=lambda x: len((x.text or "").strip()))
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", matched[0])
                time.sleep(2) # Wait longer so it is visible in the video
                
                # Removed highlight as requested
                self.dismiss_popups()
                time.sleep(1)
                
                # Force click using Javascript, try to click checkbox if available
                clicked = self.driver.execute_script("""
                    let target = arguments[0];
                    let chk = target.querySelector('input[type="checkbox"]');
                    if (!chk && target.parentElement) chk = target.parentElement.querySelector('input[type="checkbox"]');
                    if (chk) {
                        if (!chk.checked) chk.click();
                        return true;
                    }
                    target.click();
                    return true;
                """, matched[0])
                
                self.logger.info(f"Clicked filter: {filter_name}")
            else:
                self.logger.warning(f"Filter element not found for '{filter_name}'")
            
            time.sleep(3)
            self.dismiss_popups()
        except Exception as e:
            self.logger.warning(f"Filter click failed for '{filter_name}': {e}")

    def sort_low_to_high(self):
        """Sort the packages by Price: Low to High."""
        self.logger.info("Sorting by Price: Low to High")
        try:
            time.sleep(1)
            
            # Click Sort By using ActionChains
            xpath_sort = "//div[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'sort by') or contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'price:')]"
            sort_btns = self.driver.find_elements(By.XPATH, xpath_sort)
            valid_sort = [b for b in sort_btns if b.text and len(b.text.strip()) < 30]
            if valid_sort:
                valid_sort.sort(key=lambda b: len(b.text.strip()))
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", valid_sort[0])
                time.sleep(1)
                
                # Removed Highlight Sort By
                
                try:
                    ActionChains(self.driver).move_to_element(valid_sort[0]).click().perform()
                except Exception:
                    self.driver.execute_script("arguments[0].click();", valid_sort[0])
            time.sleep(2)
            
            # Click Low to High using ActionChains
            xpath_low = "//*[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'low to high')]"
            options = self.driver.find_elements(By.XPATH, xpath_low)
            valid_opts = [o for o in options if o.text and len(o.text.strip()) < 30]
            if valid_opts:
                valid_opts.sort(key=lambda o: len(o.text.strip()))
                try:
                    ActionChains(self.driver).move_to_element(valid_opts[0]).click().perform()
                except Exception:
                    self.driver.execute_script("arguments[0].click();", valid_opts[0])
            time.sleep(8)
            self.dismiss_popups()
        except Exception as e:
            self.logger.warning(f"Sort Low to High failed: {e}")
        except Exception as e:
            self.logger.warning(f"Sort Low to High failed: {e}")

    # ── Add to Cart ───────────────────────────────────────────────────────────

    def add_package_to_cart(self, package_name):
        self.logger.info(f"Adding '{package_name}' to cart")
        script = f"""
            let elements = Array.from(document.querySelectorAll('h1, h2, h3, h4, h5, p, span, div'));
            let targetNode = elements.find(el => {{
                let text = (el.textContent || '').trim();
                return text === "{package_name}" || text.includes("{package_name}");
            }});
            
            if (targetNode) {{
                let node = targetNode;
                for (let i = 0; i < 8; i++) {{
                    if (!node || !node.parentElement) break;
                    node = node.parentElement;
                    let btns = Array.from(node.querySelectorAll('button'));
                    let addBtn = btns.find(b => {{
                        let t = (b.textContent || '').trim().toLowerCase();
                        return t === 'add' || t === 'add to cart';
                    }});
                    if (addBtn) {{
                        addBtn.scrollIntoView({{block: 'center'}});
                        addBtn.click();
                        return;
                    }}
                }}
            }}
        """
        self.driver.execute_script(script)
        time.sleep(3)
        self.dismiss_popups()

    # ── Cart popup ────────────────────────────────────────────────────────────

    def proceed_to_cart_popup(self):
        """Click 'Proceed To Cart' or 'Go To Cart' on the mini-cart popup."""
        self.logger.info("Clicking 'Proceed To Cart' on popup")
        time.sleep(4) # Wait longer for popup to fully render
        
        try:
            xpath = "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'go to cart') or contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'proceed to cart')]"
            btns = self.driver.find_elements(By.XPATH, xpath)
            valid_btns = [b for b in btns if b.is_displayed()]
            if valid_btns:
                ActionChains(self.driver).move_to_element(valid_btns[-1]).click().perform()
                time.sleep(3)
                self.dismiss_popups()
                return
        except Exception:
            pass

        self.driver.execute_script("""
            let btn = Array.from(document.querySelectorAll('button, a, div')).find(el => {
                let t = (el.textContent || '').trim().toLowerCase();
                return t === 'proceed to cart' || t === 'go to cart' || t === 'proceed to cart ';
            });
            if (btn) { btn.scrollIntoView({block:'center'}); btn.click(); }
        """)
        time.sleep(3)
        self.dismiss_popups()

    # ── Patient selection ─────────────────────────────────────────────────────

    def select_patient(self, patient_name="Test User"):
        self.logger.info(f"Selecting existing patient: {patient_name}")
        
        for _ in range(15):
            try:
                # 1. Targeted JS click specifically for the patient row
                self.driver.execute_script(f"""
                    let name = '{patient_name}'.toLowerCase();
                    // Find all text nodes
                    let allNodes = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
                    let node;
                    while (node = allNodes.nextNode()) {{
                        if (node.nodeValue.toLowerCase().includes(name)) {{
                            // Found the patient name, go up and find the checkbox
                            let parent = node.parentElement;
                            for (let i = 0; i < 6; i++) {{
                                if (!parent) break;
                                let chk = parent.querySelector('input[type="checkbox"]');
                                if (chk) {{
                                    if (!chk.checked) chk.click();
                                    return;
                                }}
                                parent = parent.parentElement;
                            }}
                        }}
                    }}
                """)
                time.sleep(1)
                
                # 2. Verify if checked
                is_checked = self.driver.execute_script(f"""
                    let name = '{patient_name}'.toLowerCase();
                    let allNodes = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
                    let node;
                    while (node = allNodes.nextNode()) {{
                        if (node.nodeValue.toLowerCase().includes(name)) {{
                            let parent = node.parentElement;
                            for (let i = 0; i < 6; i++) {{
                                if (!parent) break;
                                let chk = parent.querySelector('input[type="checkbox"]');
                                if (chk) return chk.checked;
                                parent = parent.parentElement;
                            }}
                        }}
                    }}
                    return false;
                """)
                
                if is_checked:
                    self.logger.info("Patient successfully selected via JS!")
                    break
                    
                # 3. Fallback native click
                chks = self.driver.find_elements(By.XPATH, "//input[@type='checkbox']")
                if chks:
                    chk = chks[0]
                    # Only click if we are sure it's the right one (safeguard)
                    parent_div = chk.find_element(By.XPATH, "..")
                    if patient_name.lower() in parent_div.text.lower() or "mr." in parent_div.text.lower():
                        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", parent_div)
                        time.sleep(0.5)
                        ActionChains(self.driver).move_to_element(parent_div).click().perform()
                    
                    time.sleep(1)
                    if self.driver.execute_script("return arguments[0].checked;", chk):
                        self.logger.info("Patient successfully selected via NATIVE click!")
                        break
            except Exception as e:
                self.logger.warning(f"Patient select error: {e}")
            time.sleep(1)
            
        time.sleep(1.5)
        self.dismiss_popups()

        # Click 'Select Slot' button
        self.logger.info("Clicking 'Select Slot' after patient selection")
        for _ in range(10): # increased retries
            self.dismiss_popups() # Dismiss popups before trying to click
            
            # Hide tooltips that might intercept clicks
            self.driver.execute_script("""
                let tooltips = document.querySelectorAll('div[class*="tooltip"], div[class*="popup"], div[class*="toast"]');
                for (let t of tooltips) t.style.display = 'none';
            """)
            
            # Try JS click first for reliability
            clicked_js = self.driver.execute_script("""
                let b = Array.from(document.querySelectorAll('button')).find(el => {
                    let t = (el.textContent || '').toLowerCase();
                    return (t.includes('select slot') || t === 'proceed') && !t.includes('continue');
                });
                if (b) { b.click(); return true; }
                return false;
            """)
            if clicked_js:
                break
                
            # Fallback to native click
            xpath = "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'select slot') or contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'proceed')]"
            btns = self.driver.find_elements(By.XPATH, xpath)
            valid_btns = [b for b in btns if b.is_displayed()]
            
            if valid_btns:
                try:
                    ActionChains(self.driver).move_to_element(valid_btns[-1]).click().perform()
                    break
                except Exception:
                    self.driver.execute_script("arguments[0].click();", valid_btns[-1])
                    break
            time.sleep(1)
        
        time.sleep(1.5)
        self.dismiss_popups()

    def add_new_patient(self, patient_data):
        """Click Add New Patient and fill details."""
        self.logger.info("Adding new patient")
        time.sleep(2)
        # Click Add New Patient
        self.driver.execute_script("""
            let addBtn = Array.from(document.querySelectorAll('span, div, button, a')).find(el => (el.textContent || '').includes('Add New Patient'));
            if(addBtn) { addBtn.scrollIntoView({block:'center'}); addBtn.click(); }
        """)
        time.sleep(2)
        self.dismiss_popups()
        
        name = patient_data.get('patient_name', 'Test User')
        
        # Fill Form (assuming standard Name, Age inputs)
        self.driver.execute_script(f"""
            let inputs = document.querySelectorAll('input[type="text"]');
            for(let i of inputs) {{
                let p = (i.placeholder || '').toLowerCase();
                let n = (i.name || '').toLowerCase();
                if(p.includes('name') || n.includes('name')) {{
                    i.value = '{name}';
                    i.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    i.dispatchEvent(new Event('change', {{ bubbles: true }}));
                }}
            }}
            
            // Age or DOB
            let numInputs = document.querySelectorAll('input[type="number"], input[type="tel"]');
            for(let i of numInputs) {{
                let p = (i.placeholder || '').toLowerCase();
                let n = (i.name || '').toLowerCase();
                if(p.includes('age') || p.includes('year') || n.includes('age')) {{
                    i.value = '30'; // Hardcoded age for simplicity
                    i.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    i.dispatchEvent(new Event('change', {{ bubbles: true }}));
                }}
            }}
            
            // Gender (Male)
            let maleBtn = Array.from(document.querySelectorAll('span, div, button, label')).find(el => (el.textContent || '').trim() === 'Male');
            if(maleBtn) maleBtn.click();
            
            // Save / Add Patient button
            let saveBtn = Array.from(document.querySelectorAll('div[role="dialog"] button, .modal button')).find(el => {{
                let t = (el.textContent || '').toLowerCase();
                return t.includes('save') || t.includes('confirm') || t.includes('add patient');
            }});
            if(saveBtn) saveBtn.click();
            else {{
                let fallback = Array.from(document.querySelectorAll('button')).find(el => (el.textContent || '').toLowerCase().includes('save'));
                if(fallback) fallback.click();
            }}
        """)
        time.sleep(3)
        self.dismiss_popups()

        self.logger.info("Checking patient checkbox before proceeding")
        self.driver.execute_script("""
            let dialog = document.querySelector('div[role="dialog"]') || document.querySelector('.modal') || document;
            let chks = dialog.querySelectorAll('input[type="checkbox"]');
            for (let chk of chks) {
                if (!chk.checked) {
                    chk.click();
                    break;
                }
            }
        """)
        time.sleep(1)

        # Click 'Select Slot' button
        try:
            self.click_element(self.SELECT_SLOT_BTN)
        except Exception:
            self.driver.execute_script("""
                let b = Array.from(document.querySelectorAll('button'))
                             .find(el => el.textContent.includes('Select Slot'));
                if (b) b.click();
            """)
        time.sleep(2)
        self.dismiss_popups()

    # ── Address selection ─────────────────────────────────────────────────────

    def select_address(self, address_text="7/33"):
        self.logger.info(f"Selecting address containing '{address_text}'")
        
        # Fallback keyword extraction (e.g. "7a townhall" -> "7a")
        first_word = address_text.split()[0].lower().replace(',', '')
        
        # Poll up to 5s for address
        valid_els = []
        try:
            for _ in range(10):
                xpath = f"//*[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{address_text.lower()}')]"
                elements = self.driver.find_elements(By.XPATH, xpath)
                valid_els = [el for el in elements if el.text and len(el.text.strip()) < 100]
                if valid_els: break
                time.sleep(0.5)
                
            # If exact fails, try broad match using the first word or known screenshot values
            if not valid_els:
                for _ in range(4):
                    xpath = f"//*[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{first_word}') or contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '7a') or contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'town hall')]"
                    elements = self.driver.find_elements(By.XPATH, xpath)
                    valid_els = [el for el in elements if el.text and len(el.text.strip()) < 100]
                    if valid_els: break
                    time.sleep(0.5)
                
            if valid_els:
                valid_els.sort(key=lambda el: len(el.text.strip()))
                try:
                    ActionChains(self.driver).move_to_element(valid_els[0]).click().perform()
                except Exception:
                    self.driver.execute_script("arguments[0].click();", valid_els[0])
            else:
                self.logger.info("Specific address not found. Clicking first available address radio.")
                radios = self.driver.find_elements(By.XPATH, "//input[@type='radio']")
                if radios:
                    self.driver.execute_script("arguments[0].click();", radios[0])
                    
        except Exception as e:
            self.logger.warning(f"Address selection failed: {e}")
        time.sleep(1.5)
        self.dismiss_popups()

    # ── Schedule selection ────────────────────────────────────────────────────
    
    def select_schedule(self, date_str, time_str):
        self.logger.info(f"Selecting schedule: {date_str} - {time_str}")
        
        # Select Date (e.g. '22')
        day = date_str.split(' ')[0]
        
        # Poll up to 5s for dates
        for _ in range(10):
            success = self.driver.execute_script(f"""
                let day = '{day}';
                let dateEls = Array.from(document.querySelectorAll('div, span, li')).filter(el => {{
                    let t = (el.textContent || '').trim();
                    return t === day || t.includes(day + ' ');
                }});
                
                let anyDate = Array.from(document.querySelectorAll('div, span, li')).filter(el => (el.textContent || '').toLowerCase().includes('today') || (el.textContent || '').toLowerCase().includes('tomorrow'));
                
                if (dateEls.length === 0 && anyDate.length === 0) return false;
                
                let clickedDate = false;
                for(let d of dateEls) {{
                    if(d.offsetHeight > 0) {{ d.click(); clickedDate = true; break; }}
                }}
                if(!clickedDate && anyDate.length > 0) {{
                    anyDate[0].click();
                }}
                return true;
            """)
            if success:
                break
            time.sleep(0.5)
            
        time.sleep(1)
        
        # Select Time
        for _ in range(10):
            success = self.driver.execute_script(f"""
                let timeEls = Array.from(document.querySelectorAll('div, span, li')).filter(el => (el.textContent || '').includes('{time_str}'));
                let anyTime = Array.from(document.querySelectorAll('div, span, li')).filter(el => {{
                    let t = (el.textContent || '').toLowerCase();
                    return (t.includes('am') || t.includes('pm')) && t.includes(':00');
                }});
                
                if (timeEls.length === 0 && anyTime.length === 0) return false;
                
                let clickedTime = false;
                for(let t of timeEls) {{
                    if(t.offsetHeight > 0) {{ t.click(); clickedTime = true; break; }}
                }}
                if(!clickedTime && anyTime.length > 0) {{
                    anyTime[0].click();
                }}
                return true;
            """)
            if success:
                break
            time.sleep(0.5)
            
        time.sleep(1.5)
        self.dismiss_popups()

    # ── Proceed to Pay ────────────────────────────────────────────────────────

    def proceed_to_pay(self):
        self.logger.info("Clicking 'Review Cart' / Proceed")
        time.sleep(3)
        try:
            xpath = "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'review cart') or contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'proceed') or contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'continue')]"
            for _ in range(5):
                btns = self.driver.find_elements(By.XPATH, xpath)
                valid_btns = [b for b in btns if b.is_displayed() and b.text.strip()]
                if valid_btns:
                    # Prioritize the button that explicitly says "Review Cart"
                    review_btns = [b for b in valid_btns if 'review cart' in b.text.lower()]
                    target_btn = review_btns[-1] if review_btns else valid_btns[-1]
                    
                    try:
                        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", target_btn)
                        time.sleep(1)
                        ActionChains(self.driver).move_to_element(target_btn).click().perform()
                    except Exception:
                        self.logger.warning("Native click on Review Cart failed, falling back to JS click (might cause React errors)")
                        self.driver.execute_script("arguments[0].click();", target_btn)
                    break
                time.sleep(1)
        except Exception as e:
            self.logger.warning(f"Review Cart failed: {e}")
        time.sleep(5)
        self.dismiss_popups()

        self.logger.info("Clicking 'Proceed to Pay'")
        try:
            xpath = "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'proceed to pay')]"
            for _ in range(5):
                btns = self.driver.find_elements(By.XPATH, xpath)
                valid_btns = [b for b in btns if b.is_displayed()]
                if valid_btns:
                    try:
                        ActionChains(self.driver).move_to_element(valid_btns[0]).click().perform()
                    except Exception:
                        self.driver.execute_script("arguments[0].click();", valid_btns[0])
                    break
                time.sleep(1)
        except Exception as e:
            self.logger.warning(f"Proceed to Pay failed: {e}")
        time.sleep(5)
        self.dismiss_popups()

    def enter_credit_card(self, card_name="Test User", card_number="4111222233334444", exp_date="12/30", cvv="123"):
        self.logger.info("Selecting Credit Card payment method and filling details")
        
        # Poll and Click Credit Card Option
        for _ in range(10):
            xpath = "//*[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'credit card')]"
            cc_btns = self.driver.find_elements(By.XPATH, xpath)
            valid_btns = [b for b in cc_btns if b.text and len(b.text.strip()) < 30]
            if valid_btns:
                valid_btns.sort(key=lambda b: len(b.text.strip()))
                try:
                    ActionChains(self.driver).move_to_element(valid_btns[0]).click().perform()
                except Exception:
                    self.driver.execute_script("arguments[0].click();", valid_btns[0])
                break
            time.sleep(0.5)
            
        time.sleep(3)
        self.dismiss_popups()

        # Fill Dummy Details in Main Document and iFrames
        self.logger.info("Filling dummy credit card details (main and iframes)")
        for _ in range(8):
            filled_any = False
            
            def fill_current_context():
                nonlocal filled_any
                # Sometimes inputs are in a shadow root or react components
                # Try JS direct injection to trigger React events
                script = f"""
                    let filled = false;
                    let setReactValue = function(element, value) {{
                        let lastValue = element.value;
                        element.value = value;
                        let event = new Event('input', {{ bubbles: true }});
                        let tracker = element._valueTracker;
                        if (tracker) tracker.setValue(lastValue);
                        element.dispatchEvent(event);
                        element.dispatchEvent(new Event('change', {{ bubbles: true }}));
                        element.dispatchEvent(new Event('blur', {{ bubbles: true }}));
                        filled = true;
                    }};
                    
                    let inputs = document.querySelectorAll('input');
                    for (let inp of inputs) {{
                        let ph = (inp.placeholder || '').toLowerCase();
                        let n = (inp.name || '').toLowerCase();
                        let id = (inp.id || '').toLowerCase();
                        
                        if (ph.includes('name') || n.includes('name')) {{
                            if (!inp.value) setReactValue(inp, '{card_name}');
                        }} else if (ph.includes('card number') || n.includes('card_number') || ph.includes('0000')) {{
                            if (!inp.value) setReactValue(inp, '{card_number}');
                        }} else if (ph.includes('exp') || ph.includes('valid') || ph.includes('mm') || ph.includes('yy') || n.includes('exp')) {{
                            if (!inp.value) setReactValue(inp, '{exp_date}');
                        }} else if (ph.includes('cvv') || n.includes('cvv') || id.includes('cvv')) {{
                            if (!inp.value) setReactValue(inp, '{cvv}');
                        }}
                    }}
                    return filled;
                """
                try:
                    res = self.driver.execute_script(script)
                    if res: filled_any = True
                except Exception:
                    pass
                
                # Also try standard Selenium keys for good measure
                try:
                    inputs = self.driver.find_elements(By.TAG_NAME, "input")
                    for inp in inputs:
                        ph = (inp.get_attribute('placeholder') or '').lower()
                        name = (inp.get_attribute('name') or '').lower()
                        id_attr = (inp.get_attribute('id') or '').lower()
                        
                        if 'name' in ph or 'name' in name or 'name' in id_attr:
                            if not inp.get_attribute('value'):
                                inp.send_keys(card_name)
                                filled_any = True
                        elif 'card number' in ph or 'card_number' in name or 'card_number' in id_attr or '0000' in ph:
                            if not inp.get_attribute('value'):
                                inp.send_keys(card_number)
                                filled_any = True
                        elif 'exp' in ph or 'valid' in ph or 'mm/yy' in ph or 'mm / yy' in ph or 'exp' in name:
                            if not inp.get_attribute('value'):
                                inp.send_keys(exp_date)
                                filled_any = True
                        elif 'cvv' in ph or 'cvv' in name or 'cvv' in id_attr:
                            if not inp.get_attribute('value'):
                                inp.send_keys(cvv)
                                filled_any = True
                except Exception:
                    pass
                        
            # Try main document first
            self.driver.switch_to.default_content()
            fill_current_context()
            
            # Try all iframes
            iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
            for iframe in iframes:
                try:
                    self.driver.switch_to.default_content()
                    self.driver.switch_to.frame(iframe)
                    fill_current_context()
                except Exception:
                    pass
                finally:
                    self.driver.switch_to.default_content()
            
            if filled_any:
                break
            time.sleep(1.5)

        time.sleep(2)
        
        # Click Pay button
        self.logger.info("Clicking Pay Button")
        try:
            self.driver.execute_script("""
                let payBtns = Array.from(document.querySelectorAll('button')).filter(b => {
                    let t = (b.textContent || '').toLowerCase();
                    return t.includes('pay ') || t === 'pay';
                });
                if(payBtns.length > 0) {
                    payBtns[0].scrollIntoView({block: 'center'});
                    payBtns[0].click();
                }
            """)
        except Exception as e:
            self.logger.warning(f"Failed to click Pay button: {e}")
            
        time.sleep(3)
        self.dismiss_popups()

