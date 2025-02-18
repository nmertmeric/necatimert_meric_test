import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Test_Automation.utils.browser_utils import initialize_browser
from Test_Automation.pages.home_page import HomePage
from Test_Automation.pages.carrier_page import CarrierPage
from Test_Automation.pages.team_pages.qa_team_page import QATeamPage


# Fixture to initialize and close the browser
@pytest.fixture(scope="module")
def driver():
    browser_name = "chrome"  # Change this to "firefox" for Firefox
    driver = initialize_browser(browser_name)
    driver.maximize_window()
    yield driver
    driver.quit()


# Fixture to initialize page objects
@pytest.fixture(scope="module")
def pages(driver):
    home_page = HomePage(driver)
    carrier_page = CarrierPage(driver)
    qa_team_page = QATeamPage(driver)
    return home_page, carrier_page, qa_team_page


def test_insider_home_page(driver, pages):
    """1. Visit https://useinsider.com/ and check Insider home page is opened or not."""
    home_page, _, _ = pages
    home_page.navigate_insider_page_url()


def test_career_page_blocks(driver, pages):
    """2. Select the “Company” menu, select “Careers”, and check Career page blocks."""
    home_page, carrier_page, _ = pages

    # Navigate to Careers page
    home_page.navigate_to_careers()
    assert carrier_page.verify_carrier_page(), "Carrier page is not loaded!"

    # Verify Teams block
    assert carrier_page.verify_teams_block(), "Teams block is not as expected!"

    # Click "See All Teams" and verify Locations block
    carrier_page.click_see_all_teams()
    assert carrier_page.verify_locations_block(), "Locations block is not as expected!"

    # Verify Life at Insider block
    assert carrier_page.verify_life_block(), "Life at Insider block is not as expected!"


def test_qa_jobs_page(driver, pages):
    """3. Go to QA jobs page, filter jobs by Location and Department, and check job list."""
    _, carrier_page, qa_team_page = pages

    # Navigate to QA Team page
    carrier_page.click_qa_team_field()
    assert qa_team_page.verify_qa_job_page(), "QA Team page is not loaded!"

    # Click "See All QA Jobs" and filter jobs
    qa_team_page.click_see_all_qa_jobs_button()
    qa_team_page.select_qa_jobs_in_istanbul()

    # Verify job list
    assert qa_team_page.verify_qa_job_list(), "Could not find the job list"


def test_verify_jobs(driver, pages):
    """4. Check that all jobs’ Position, Department, and Location match the criteria."""
    _, _, qa_team_page = pages
    qa_team_page.verify_jobs()


def test_view_role_redirect(driver, pages):
    """5. Click the “View Role” button and check redirection to Lever Application form page."""
    _, _, qa_team_page = pages

    # Scroll to the first job and verify redirection
    qa_team_page.scroll_to_first_job()
    qa_team_page.hover_over_and_verify_jobs()

