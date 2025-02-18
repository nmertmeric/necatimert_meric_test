import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService

def initialize_browser(browser_name):
    """
    Initialize the browser driver based on the selected browser.
    :param browser_name: Name of the browser (chrome, firefox).
    :return: WebDriver instance.
    """
    if browser_name.lower() == "chrome":
        return webdriver.Chrome(service=ChromeService())
    elif browser_name.lower() == "firefox":
        return webdriver.Firefox(service=FirefoxService())
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")