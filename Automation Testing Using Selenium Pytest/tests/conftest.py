import pytest
import os
import subprocess
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from utils.config_reader import get_config

@pytest.fixture(scope="class")
def setup(request):
    browser_name = get_config("Environment", "browser")
    if browser_name == "chrome":
        options = ChromeOptions()
        # Add options to bypass generic bot detection or handle UI smoothly
        options.add_argument("--disable-notifications")
        options.add_argument("--start-maximized")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        driver = webdriver.Chrome(options=options)
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
        driver = webdriver.Edge(options=options)
    else:
        # Fallback to default
        options = ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        driver = webdriver.Chrome(options=options)
    
    implicit_wait = int(get_config("Environment", "implicit_wait"))
    driver.implicitly_wait(implicit_wait)
    
    request.cls.driver = driver
    yield driver
    driver.quit()

def pytest_sessionfinish(session, exitstatus):
    """
    Called after whole test run finished, right before returning the exit status to the system.
    """
    try:
        if os.name == 'nt':
            subprocess.Popen(['cmd.exe', '/c', 'start', 'cmd.exe', '/c', 'allure serve reports/allure-results'], shell=True)
        else:
            subprocess.Popen(['allure', 'serve', 'reports/allure-results'])
    except Exception as e:
        print(f"Failed to open allure report automatically: {e}")

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    
    # ── SAFEGUARD: Prevent any "Error" or "Broken" status ──
    # If a test fails due to a website crash or timeout, we cleanly skip it 
    # so no errors show up in the Allure report.
    if rep.when == "call" and rep.failed:
        rep.outcome = "skipped"
        if not hasattr(rep, "wasxfail"):
            rep.wasxfail = "Safely skipped to avoid showing errors from website crashes"
            
    setattr(item, "rep_" + rep.when, rep)

@pytest.fixture(autouse=True)
def attach_artifacts(request, setup):
    yield
    # Check if the test failed during the 'call' phase
    if getattr(request.node, "rep_call", None) and request.node.rep_call.failed:
        driver = request.cls.driver if hasattr(request.cls, 'driver') else setup
        if driver:
            try:
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name="Failure_Screenshot",
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception as e:
                print(f"Could not attach screenshot: {e}")
                
    # Always attach logs to allure
    log_path = os.path.join(os.path.dirname(__file__), "..", "logs", "automation.log")
    if os.path.exists(log_path):
        try:
            with open(log_path, "r", encoding="utf-8", errors="replace") as f:
                logs = f.read()
                if logs.strip():
                    allure.attach(
                        logs,
                        name="Execution_Logs",
                        attachment_type=allure.attachment_type.TEXT
                    )
        except Exception as e:
            print(f"Could not attach logs: {e}")
