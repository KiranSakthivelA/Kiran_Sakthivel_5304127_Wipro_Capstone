import subprocess
import os
import shutil
import sys

if __name__ == "__main__":
    print("Starting BDD Test Execution with Behave...")
    
    # Clean up old allure results to prevent duplicate attachments
    results_dir = "reports/allure-results"
    if os.path.exists(results_dir):
        shutil.rmtree(results_dir)
    os.makedirs(results_dir, exist_ok=True)
    
    # Run behave with explicit formatter
    subprocess.run([sys.executable, "-m", "behave", "-f", "allure_behave.formatter:AllureFormatter", "-o", results_dir, "./features"], shell=True)
    
    # Generate and serve allure report
    print("Generating Allure Report...")
    if os.name == 'nt':
        subprocess.Popen(['cmd.exe', '/c', 'start', 'cmd.exe', '/c', 'allure serve reports/allure-results'], shell=True)
    else:
        subprocess.Popen(['allure', 'serve', 'reports/allure-results'])
