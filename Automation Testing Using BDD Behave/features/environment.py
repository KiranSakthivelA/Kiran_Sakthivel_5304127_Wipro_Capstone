import os
import allure
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from utils.config_reader import get_config

def before_scenario(context, scenario):
    browser_name = get_config("Environment", "browser")
    if browser_name == "chrome":
        options = ChromeOptions()
        options.add_argument("--disable-notifications")
        options.add_argument("--start-maximized")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        context.driver = webdriver.Chrome(options=options)
    elif browser_name == "edge":
        from selenium.webdriver.edge.options import Options as EdgeOptions
        options = EdgeOptions()
        options.add_argument("--disable-notifications")
        options.add_argument("--start-maximized")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        context.driver = webdriver.Edge(options=options)
    else:
        options = ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        context.driver = webdriver.Chrome(options=options)
    
    implicit_wait = int(get_config("Environment", "implicit_wait"))
    context.driver.implicitly_wait(implicit_wait)

def after_step(context, step):
    if step.status == "failed":
        if hasattr(context, "driver"):
            try:
                allure.attach(
                    context.driver.get_screenshot_as_png(),
                    name=f"Failure_Screenshot_{step.name}",
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception as e:
                print(f"Could not attach screenshot: {e}")
                
        # Attach logs on failure to satisfy defect handling requirement
        log_path = os.path.join(os.path.dirname(__file__), "..", "logs", "automation.log")
        if os.path.exists(log_path):
            try:
                with open(log_path, "r", encoding="utf-8", errors="replace") as f:
                    logs = f.read()
                    if logs.strip():
                        allure.attach(
                            logs,
                            name=f"Failure_Logs_{step.name}",
                            attachment_type=allure.attachment_type.TEXT
                        )
            except Exception as e:
                print(f"Could not attach logs: {e}")

def after_scenario(context, scenario):
    if hasattr(context, "driver"):
        context.driver.quit()
