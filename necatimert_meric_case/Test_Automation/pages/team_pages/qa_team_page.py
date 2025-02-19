from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Test_Automation.utils.web_utils import WebUtils
import time

class QATeamPage(WebUtils):
    # QA Team Page
    QA_TEAM_PAGE_TITLE = (By.CSS_SELECTOR, ".big-title")
    SEE_ALL_QA_JOBS_BUTTON = (By.CSS_SELECTOR, ".btn-outline-secondary")

    # Filters
    FILTER_BY_LOCATION = (By.ID, "select2-filter-by-location-container")
    FILTER_BY_DEPARTMENT = (By.ID, "select2-filter-by-department-container")
    LOCATION_OPTION_ISTANBUL = (By.CSS_SELECTOR, "li.select2-results__option[data-select2-id*='Istanbul']")
    DEPARTMENT_OPTION_QA = (By.XPATH, "//li[contains(text(), 'Quality Assurance')]")

    # Job Listings
    JOB_LIST_CONTAINER = (By.ID, "career-position-list")
    JOB_LIST = (By.ID, "jobs-list")
    JOB_POSITION_ITEM = (By.CSS_SELECTOR, ".position-list-item")
    JOB_POSITION_TITLE = (By.CSS_SELECTOR, ".position-title")
    JOB_POSITION_DEPARTMENT = (By.CSS_SELECTOR, ".position-department")
    JOB_POSITION_LOCATION = (By.CSS_SELECTOR, ".position-location")

    # Specific Job Listings (Istanbul)
    FIRST_JOB_IN_ISTANBUL = (By.CSS_SELECTOR, '.position-list-item[data-location="istanbul-turkiye"]:nth-child(1)')
    ALL_JOBS_IN_ISTANBUL = (By.CSS_SELECTOR, '.position-list-item[data-location="istanbul-turkiye"]')

    # View Role Button
    VIEW_ROLE_BUTTON = (By.CSS_SELECTOR, '.btn.btn-navy.rounded.pt-2.pr-5.pb-2.pl-5')

    # Lever Page
    LEVER_JOB_POSITION_TITLE = (By.CSS_SELECTOR, ".posting-headline > h2")
    LEVER_APPLY_FOR_JOB_BUTTON = (By.CSS_SELECTOR, ".postings-btn-wrapper > a")


    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def verify_qa_job_page(self):
        """Verify the QA Team page is loaded."""
        return self.get_element(self.QA_TEAM_PAGE_TITLE)

    def verify_qa_job_list(self):
        """Verify the QA Team page is loaded."""
        return self.get_element(self.JOB_LIST)

    def click_see_all_qa_jobs_button(self):
        """Click on the 'See all QA jobs' button."""
        self.click_on(self.SEE_ALL_QA_JOBS_BUTTON)


    def select_qa_jobs_in_istanbul(self):
        time.sleep(20) # I need to wait since another dropdown menu appears if I click it early
        self.click_on(self.FILTER_BY_LOCATION)
        self.click_on(self.LOCATION_OPTION_ISTANBUL)
        self.click_on(self.FILTER_BY_DEPARTMENT)
        self.click_on(self.DEPARTMENT_OPTION_QA)
        time.sleep(5) # Wait for job list refresh


    def scroll_to_first_job(self):
        """Scroll to and verify 'Life at Insider' section."""
        element_text = self.scroll_and_get_element(self.FIRST_JOB_IN_ISTANBUL)
        return element_text


    def verify_jobs(self):
        """
        Verify that all listed jobs meet the criteria:
        - Position contains "Quality Assurance"
        - Department contains "Quality Assurance"
        - Location contains "Istanbul, Turkey"
        """
        try:
            # Find all job elements
            jobs = self.get_elements(self.JOB_POSITION_ITEM)

            # Initialize a flag to track if all jobs meet the criteria
            all_jobs_valid = True

            # Iterate through each job and verify the criteria
            for job in jobs:
                try:
                    # Extract Position, Department, and Location
                    position = job.find_element(*self.JOB_POSITION_TITLE).text
                    department = job.find_element(*self.JOB_POSITION_DEPARTMENT).text
                    location = job.find_element(*self.JOB_POSITION_LOCATION).text

                    # Verify the criteria
                    if "Quality Assurance" not in position and "QA" not in position:
                        print(f"Position does not contain 'Quality Assurance': {position}")
                        all_jobs_valid = False
                    if "Quality Assurance" not in department and "QA" not in department:
                        print(f"Department does not contain 'Quality Assurance': {department}")
                        all_jobs_valid = False
                    if "Istanbul, Turkiye" not in location:
                        print(f"Location does not contain 'Istanbul, Turkiye': {location}")
                        all_jobs_valid = False
                    #Job Details
                    print(f"Job Details - Position: {position}, Department: {department}, Location: {location}")

                except NoSuchElementException:
                    print("Could not extract job details. Skipping this job.")
                    all_jobs_valid = False

            if all_jobs_valid:
                print("All jobs meet the criteria!")
            else:
                print("Some jobs do not meet the criteria.")

        except TimeoutException:
            print("Job list did not load within the timeout period.")
        except Exception as e:
            print(f"An error occurred: {e}")


    def hover_over_and_verify_jobs(self):
        """
        Hover over each job element, click the 'View Role' button, verify redirection,
        check the position title and 'Apply for this job' button on the Lever page.
        """
        try:
            # Locate all job elements
            jobs = self.get_elements(self.ALL_JOBS_IN_ISTANBUL)

            # Save the main tab handle
            main_tab = self.driver.current_window_handle

            # Iterate through each job
            for job in jobs:
                try:
                    # Hover over the job element
                    self.hover_over_an_element(job)
                    print("Hovered over a job element.")
                    time.sleep(1)  # Pause for visibility

                    # Locate the position title in the job element using job_position_title_list
                    position_title = job.find_element(*self.JOB_POSITION_TITLE).text
                    print(f"Found position title: {position_title}")

                    # Locate and click the "View Role" button within the job element
                    view_role_button = job.find_element(*self.VIEW_ROLE_BUTTON)
                    self.click_on(view_role_button)
                    print(f"Clicked the 'View Role' button for position: {position_title}.")

                    # Switch to the newly opened tab
                    new_tab = [tab for tab in self.driver.window_handles if tab != main_tab][0]
                    self.driver.switch_to.window(new_tab)
                    print("Switched to the new tab.")

                    # Wait for the URL to change to Lever's page
                    WebDriverWait(self.driver, self.time_to_wait, poll_frequency=2).until(
                        EC.url_contains("lever.co")
                    )
                    print("Redirected to Lever page.")

                    # Verify the headline element on the redirected page
                    WebDriverWait(self.driver, self.time_to_wait, poll_frequency=2).until(
                        EC.visibility_of_element_located(
                            (By.CSS_SELECTOR, "div.posting-header div.posting-headline h2"))
                    )
                    print("Headline element is visible on the redirected page.")

                    # Verify the position title exists on the Lever page
                    try:
                        lever_position_title = self.get_element_text(self.LEVER_JOB_POSITION_TITLE)
                        if position_title not in lever_position_title:
                            print(
                                f"Position mismatch: Expected '{position_title}', but found '{lever_position_title}' on the Lever page.")
                        else:
                            print(f"Verified position title '{position_title}' on the Lever page.")

                        # Verify the 'Apply for this job' button exists
                        apply_button = self.get_element(self.LEVER_APPLY_FOR_JOB_BUTTON)
                        if apply_button.is_displayed():
                            print("Verified 'Apply for this job' button exists.")
                        else:
                            print("'Apply for this job' button is not visible.")

                        self.driver.close()
                        self.driver.switch_to.window(main_tab)
                        time.sleep(5)  # Pause for stability
                        print("Closed the new tab and returned to the main tab.")

                    except NoSuchElementException:
                        print("Required elements (position title or apply button) not found on the Lever page.")

                except NoSuchElementException:
                    print("Could not find the 'View Role' button or position title for this job.")
                except TimeoutException:
                    print("Timed out waiting for the Lever Application form page to load.")
                except Exception as e:
                    print(f"An error occurred: {e}")

        except NoSuchElementException:
            print("No job elements found.")
        except Exception as e:
            print(f"An error occurred: {e}")
