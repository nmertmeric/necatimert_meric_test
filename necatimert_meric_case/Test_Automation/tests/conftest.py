import os
import time
from Test_Automation.utils.screenshot_utils import take_screenshot  # Assuming you have this utility already
import pytest

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture a screenshot when a test fails."""
    outcome = yield
    result = outcome.get_result()

    # Get the project directory
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Check if the test failed during the "call" phase
    if result.when == "call" and result.failed:
        # Get the driver used in the test from the fixture
        driver = item.funcargs.get("driver")
        if driver:
            # Generate a screenshot name based on the test name and timestamp
            screenshot_name = f"{item.nodeid.replace('::', '_')}_{int(time.time())}.png"

            # Define the path where the screenshot will be saved
            screenshot_path = os.path.join(project_dir, "output", "screenshots", screenshot_name)

            # Ensure the directory exists
            os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)

            # Take the screenshot using your existing utility
            take_screenshot(driver, screenshot_path)
            print(f"Screenshot saved: {screenshot_path}")
