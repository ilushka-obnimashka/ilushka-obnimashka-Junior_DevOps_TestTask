import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


@pytest.fixture(scope="session")
def base_url():
    return os.getenv("BASE_URL", "http://localhost:8080").rstrip("/")


@pytest.fixture
def browser():
    options = webdriver.ChromeOptions()
    if os.getenv("HEADLESS", "1") != "0":
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1440,1000")
    options.add_argument("--disable-dev-shm-usage")
    if os.getenv("CHROME_NO_SANDBOX") == "1":
        options.add_argument("--no-sandbox")
    if binary := os.getenv("CHROME_BINARY"):
        options.binary_location = binary
    options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
    driver_path = os.getenv("CHROMEDRIVER")
    service = Service(driver_path) if driver_path else Service()
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_page_load_timeout(100)
    driver.execute_cdp_cmd("Network.enable", {})
    try:
        yield driver
    finally:
        driver.quit()
