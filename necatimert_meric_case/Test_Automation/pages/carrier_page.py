from selenium.webdriver.common.by import By
from Test_Automation.utils.web_utils import WebUtils


class CarrierPage(WebUtils):
    # Locators
    CAREER_PAGE = (By.CLASS_NAME, "career-page")
    CAREER_PAGE_TEAMS = (By.CLASS_NAME, "job-title.mt-0.mt-lg-2.mt-xl-5")
    SEE_ALL_TEAMS_BUTTON = (By.CSS_SELECTOR, "a.btn:nth-child(3)")
    OUR_LOCATIONS = (By.CSS_SELECTOR, ".ml-0")
    FIND_YOUR_CALLING = (By.CSS_SELECTOR, "div.mb-xl-5 > h3")
    LIFE_AT_INSIDER = (By.CSS_SELECTOR, ".elementor-element-21cea83 > div > h2")

    # Quality Assurance Team
    QUALITY_ASSURANCE_TEAM_FIELD = (By.CSS_SELECTOR, "div.job-item:nth-child(23) > div > a > h3")

    EXPECTED_TEAMS_BLOCK_TEXT = "Find your calling"
    EXPECTED_LOCATIONS_BLOCK_TEXT = "Our Locations"
    EXPECTED_LIFE_BLOCK_TEXT = "Life at Insider"

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver


    def verify_carrier_page(self):
        """Verify the Carrier page is loaded."""
        return self.get_element(self.CAREER_PAGE)


    def click_see_all_teams(self):
        """Click on the 'See All Teams' button."""
        self.scroll_and_click(self.SEE_ALL_TEAMS_BUTTON)


    def scroll_to_find_your_calling(self):
        """Scroll to and verify 'Find Your Calling' section."""
        element_text = self.scroll_and_get_element(self.FIND_YOUR_CALLING)
        return element_text


    def scroll_to_our_locations(self):
        """Scroll to and verify 'Our Locations' section."""
        element_text = self.scroll_and_get_element(self.OUR_LOCATIONS)
        return element_text  # Return the text content of the section


    def scroll_to_life_at_insider(self):
        """Scroll to and verify 'Life at Insider' section."""
        element_text = self.scroll_and_get_element(self.LIFE_AT_INSIDER)
        return element_text


    def click_qa_team_field(self):
        """Click on the 'QA Jobs' button."""
        self.scroll_and_click(self.QUALITY_ASSURANCE_TEAM_FIELD)


    def verify_teams_block(self):
        teams_block_text = self.scroll_to_find_your_calling()
        return teams_block_text == self.EXPECTED_TEAMS_BLOCK_TEXT


    def verify_locations_block(self):
        locations_block_text = self.scroll_to_our_locations()
        return locations_block_text == self.EXPECTED_LOCATIONS_BLOCK_TEXT


    def verify_life_block(self):
        life_block_text = self.scroll_to_life_at_insider()
        return life_block_text == self.EXPECTED_LIFE_BLOCK_TEXT
