import os
import allure
from utils.logger import get_and_clear_step_logs

def capture_screenshot(driver, name):
    screenshot_dir = os.path.join(os.path.dirname(__file__), "..", "reports", "screenshots")
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)
    
    file_path = os.path.join(screenshot_dir, f"{name}.png")
    driver.save_screenshot(file_path)
    
    allure.attach(driver.get_screenshot_as_png(), name=name, attachment_type=allure.attachment_type.PNG)
    
    step_logs = get_and_clear_step_logs()
    if step_logs:
        allure.attach(step_logs, name=f"Logs for {name}", attachment_type=allure.attachment_type.TEXT)
        
    return file_path
