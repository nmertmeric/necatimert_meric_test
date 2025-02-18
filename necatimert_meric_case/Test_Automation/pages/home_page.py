import time
from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from Test_Automation.utils.web_utils import WebUtils


class HomePage(WebUtils):
    # Locators
    CAREERS_LINK = (By.XPATH, "//a[text()='Careers']")
    COMPANY_MENU = (By.CSS_SELECTOR, "li.nav-item:nth-child(6)")

    # Home Page
    HOME_PAGE = (By.CLASS_NAME, "home-page")

    # Cookie Consent
    COOKIE_ACCEPT_BUTTON = (By.CSS_SELECTOR, "#wt-cli-accept-all-btn")

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver


    def navigate_insider_page_url(self):
        """Navigate to Insider homepage."""
        self.driver.get("https://useinsider.com")
        self.get_element(self.HOME_PAGE)
        self.handle_cookie_notification()


    def handle_cookie_notification(self):
        """Handle the cookie notification by accepting it."""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                WebDriverWait(self.driver, self.time_to_wait).until(
                    EC.presence_of_element_located(self.COOKIE_ACCEPT_BUTTON)
                )
                cookie_button = self.driver.find_element(*self.COOKIE_ACCEPT_BUTTON)
                cookie_button.click()
                print("Cookie notification accepted.")
                time.sleep(2)
                break
            except TimeoutException:
                print(f"Attempt {attempt + 1}: Cookie notification not found. Retrying...")
                time.sleep(2)
        else:
            print("Cookie notification could not be found after multiple attempts.")


    def navigate_to_careers(self):
        """Navigate to the Careers page from the homepage."""
        self.click_on(self.COMPANY_MENU)
        self.click_on(self.CAREERS_LINK)

