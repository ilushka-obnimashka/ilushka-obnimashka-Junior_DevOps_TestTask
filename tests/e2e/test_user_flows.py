import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

pytestmark = pytest.mark.e2e


def test_accept_and_reset(browser, base_url):
    browser.get(base_url)
    wait = WebDriverWait(browser, 100)

    wait.until(EC.element_to_be_clickable((By.ID, "accept"))).click()

    panel = wait.until(EC.visibility_of_element_located((By.ID, "match-panel")))

    assert panel.is_displayed()
    assert browser.find_element(By.ID, "match-message").text == (
        "Вы ищете DevOps. Я ищу команду. Мы идеально подходим друг-другу 💙"
    )
    assert not browser.find_element(By.ID, "candidate").is_displayed()

    browser.find_element(By.ID, "again").click()

    wait.until(EC.visibility_of_element_located((By.ID, "candidate")))
    assert not panel.is_displayed()


def test_notification_can_be_closed(browser, base_url):
    browser.get(base_url)
    wait = WebDriverWait(browser, 100)

    wait.until(EC.element_to_be_clickable((By.ID, "notification"))).click()

    toast = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#toast-area .toast")))

    assert toast.find_element(By.TAG_NAME, "span").text.strip()

    toast.find_element(By.TAG_NAME, "button").click()

    wait.until(EC.staleness_of(toast))
