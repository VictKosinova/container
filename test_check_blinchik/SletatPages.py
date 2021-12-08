from BaseApp import BasePage
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
from selenium.webdriver.support import expected_conditions


class SletatSeacrhLocators:
    LOCATOR_SEARCH_FIELD = (By.XPATH, "/html/body/div[1]/div[2]/div[1]/div/div[1]/section/div[1]/section[1]/fieldset/div/fieldset/input")
    LOCATOR_SEARCH_BUTTON = (By.XPATH, "/html/body/div[1]/div[2]/div[1]/div/div[1]/section/footer/section[2]/button")
    LOCATOR_BLINCHIC = (By.XPATH, "/html/body/div[1]/div[2]/div[1]/div/div[3]/div[3]")


class SearchHelper(BasePage):

    def enter_word(self, word):
        time.sleep(10)
        search_field = self.find_element(SletatSeacrhLocators.LOCATOR_SEARCH_FIELD)
        time.sleep(10)
        search_field.click()
        search_field.send_keys(word)
        return search_field

    def click_on_the_search_button(self):
        return self.find_element(SletatSeacrhLocators.LOCATOR_SEARCH_BUTTON, time=20).click()

    def check_blinchik_exist(self):
            try:
                self.find_element(SletatSeacrhLocators.LOCATOR_BLINCHIC)
            except NoSuchElementException:
                return False
            return "Exist"
