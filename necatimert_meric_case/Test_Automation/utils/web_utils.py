from selenium.common import ElementNotVisibleException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
import time



class WebUtils:

    def __init__(self, driver):
        self.driver = driver
        self.time_to_wait = 30


    def click_on(self, by_locator):
        WebDriverWait(self.driver, self.time_to_wait).until(EC.element_to_be_clickable(by_locator)).click()


    def enter_text(self, by_locator, text):
        WebDriverWait(self.driver, self.time_to_wait).until(EC.visibility_of_element_located(by_locator)).send_keys(
            text)


    def get_element_text(self, by_locator):
        return WebDriverWait(self.driver, self.time_to_wait).until(EC.visibility_of_element_located(by_locator)).text


    def get_element(self, by_locator):
        return WebDriverWait(self.driver, self.time_to_wait).until(EC.visibility_of_element_located(by_locator))


    def get_elements(self, by_locator):
        return WebDriverWait(self.driver, self.time_to_wait).until(
            EC.visibility_of_all_elements_located(by_locator)
        )


    def hover_over_an_element(self, by_locator):
        element = WebDriverWait(self.driver, self.time_to_wait).until(EC.element_to_be_clickable(by_locator))
        hover_action = ActionChains(self.driver).move_to_element(element)
        hover_action.perform()


    def scroll_and_click(self, by_locator):
        """
        Scrolls to an element, ensures it is fully within the viewport, and clicks it.
        Handles Firefox's out-of-bounds issue and retries if necessary.
        """
        try:
            # Locate the target element
            button = self.driver.find_element(*by_locator)
        except NoSuchElementException:
            print(f"Element with locator {by_locator} not found.")
            return

        try:
            # Scroll the element into the center of the viewport
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", button)

            # Add a small offset to ensure the element is fully visible
            self.driver.execute_script("window.scrollBy(0, -100);")  # Scroll up by 100 pixels

            # Wait for the element to be clickable
            WebDriverWait(self.driver, self.time_to_wait).until(
                EC.element_to_be_clickable(button)
            )

            # Use JavaScript to click the element directly (bypassing ActionChains)
            self.driver.execute_script("arguments[0].click();", button)
            print(f"Successfully clicked the See All Teams button")

        except TimeoutException:
            print("Element is not clickable within the timeout period.")
        except ElementClickInterceptedException:
            print("Element click intercepted, retrying...")
            time.sleep(2)  # Wait a bit and retry
            self.driver.execute_script("arguments[0].click();", button)
        except Exception as e:
            print(f"An error occurred: {e}")


    def scroll_and_get_element(self, by_locator):
        """
        Scrolls to an element, waits for it to be visible, and returns its text.

        :param by_locator: A tuple containing the locator strategy and the locator value (e.g., (By.CSS_SELECTOR, ".btn"))
        :return: Text of the element (or None if the element is not found or not visible)
        """
        # Locate the target element
        try:
            element = self.driver.find_element(*by_locator)
        except NoSuchElementException:
            print(f"Element with locator {by_locator} not found.")
            return None

        time.sleep(2)
        # Scroll the element into the center of the viewport
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element)


        # Wait for the element to be visible
        try:
            WebDriverWait(self.driver, self.time_to_wait).until(
                EC.visibility_of_element_located(by_locator)
            )
        except TimeoutException:
            print("Element is not visible within the timeout period.")
            return None

        # Get the element's text
        element_text = element.text
        print(f"element_text: {element_text}")
        time.sleep(2)
        return element_text
