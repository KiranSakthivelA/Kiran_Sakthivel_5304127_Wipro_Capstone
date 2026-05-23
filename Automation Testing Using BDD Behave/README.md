# 🏥 Apollo 24/7 – Lab Test Module - Capstone Project
### Selenium + Pytest + Allure | Complete End-to-End Automation

---

## 📌 Project Overview

Complete end-to-end test automation for the **Apollo 24/7 Lab Test Checkout** flow.

| Attribute        | Details                                  |
|------------------|------------------------------------------|
| **Application**  | Apollo 24/7 – Lab Tests Module           |
| **Module**       | Popular Health Checkup + Complete Checkout |
| **Tool Stack**   | Python · Selenium · Pytest · Allure      |
| **Framework**    | Page Object Model (POM)                  |
| **Test Cases**   | 8 Test Cases (4 Positive + 4 Negative)   |
| **Parameterization** | CSV-based (NO Hardcoding)             |
| **Browser**      | Google Chrome (configurable)             |
| **Target Score** | 70+ points (Evaluation Criteria)          |

---

## 🗂️ Project Structure

```
Wipro_Capstone_Project/
│
├── config/
│   └── config.properties        ← Browser, URL, wait timeouts
│
├── data/
│   └── popular_packages_data.csv ← Data-driven test input (8 packages)
│
├── pages/
│   ├── basepage.py              ← Abstract base class (WebDriverWait wrappers)
│   └── labtestspage.py         ← Page Object for Lab Tests (locators + actions)
│
├── tests/
│   ├── conftest.py              ← Pytest fixtures (browser setup, screenshots)
│   └── test_popular_health_checkup.py  ← 13 Test cases with Allure annotations
│
├── utils/
│   ├── config_reader.py         ← Reads config.properties
│   ├── logger.py                ← File-based logger (daily log rotation)
│   ├── screenshot_util.py       ← Auto-screenshot on failure + Allure attach
│   ├── csv_reader.py            ← CSV data reader utility
│   └── excel_reader.py          ← Excel data reader utility
│
├── logs/                        ← Generated: automation_YYYYMMDD.log
├── reports/
│   ├── allure-results/          ← Generated: Allure raw results
│   └── screenshots/             ← Generated: Failure screenshots
│
├── conftest.py                  ← Root path configuration
├── pytest.ini                   ← Pytest configuration + Allure directory
└── requirements.txt             ← Python dependencies
```

---

## ⚙️ Setup & Installation

```bash
# 1. Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate       # Windows

# 2. Install all dependencies
pip install -r requirements.txt

# 3. Ensure ChromeDriver matches your Chrome version
#    (Selenium 4+ uses Selenium Manager – auto-managed)
```

---

## ▶️ Running the Tests

```bash
# Run all 13 test cases with verbose output
pytest

# Run a specific test case
pytest tests/test_popular_health_checkup.py::TestPopularHealthCheckup::test_tc01_page_loads -v

# Run with HTML report
pytest --html=reports/report.html
```

---

## 📊 Generating Allure Report

```bash
# Step 1: Run tests (results go to reports/allure-results/)
pytest

# Step 2: Serve the Allure dashboard
allure serve reports/allure-results
```

---

## 🧪 Test Cases Summary

| TC   | Title                                        | Severity  | Type     |
|------|----------------------------------------------|-----------|----------|
| TC01 | Page loads successfully                      | BLOCKER   | Positive |
| TC02 | Popup/modal dismissed on page load           | CRITICAL  | Positive |
| TC03 | Popular Health Checkup section is visible    | CRITICAL  | Positive |
| TC04 | Section heading contains 'Popular' keyword   | NORMAL    | Positive |
| TC05 | At least 1 package card displayed            | CRITICAL  | Positive |
| TC06 | Every package card has a non-empty title     | NORMAL    | Positive |
| TC07 | Every package card shows a price             | NORMAL    | Positive |
| TC08 | Prices display the ₹ (Rupee) symbol          | MINOR     | Positive |
| TC09 | Book Now / Add to Cart buttons present       | NORMAL    | Positive |
| TC10 | Number of CTAs matches number of cards       | MINOR     | Positive |
| TC11 | First package card has title, price & CTA   | NORMAL    | Positive |
| TC12 | POSITIVE: Heading matches expected pattern   | NORMAL    | Positive |
| TC13 | NEGATIVE: Heading has NO irrelevant text     | MINOR     | Negative |

---

## 🔑 Key Technical Highlights

- **POM Architecture** – `BasePage` abstracts all Selenium interactions; `LabTestsPage` only contains locators and business logic
- **Multi-Strategy Locators** – Each element has 2–3 XPath fallback strategies to handle Apollo 247's A/B UI variations
- **Popup Handling** – ESC key + button click + backdrop click (3 strategies in sequence)
- **Allure Integration** – Epic/Feature/Story hierarchy + auto-screenshot on failure
- **Config-Driven** – Browser, URL, and wait timeouts externalized to `config.properties`
- **Data-Driven Ready** – CSV file with 8 health packages for parameterized tests
- **Logging** – Daily rotating log file + live console output during test runs

---

## 👤 Author

**Wipro Capstone Project**  
Module: Apollo 247 Lab Tests – Popular Health Checkup Packages Automation
