from BaseApp import BasePage
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
import time


class SletatSeacrhLocators:
    LOCATOR_SEARCH_FIELD = (By.XPATH, "/html/body/div[1]/div[2]/div[1]/div/div[1]/section/div[1]/section[1]/fieldset/div/fieldset/input")
    LOCATOR_SEARCH_BUTTON = (By.XPATH, "/html/body/div[1]/div[2]/div[1]/div/div[1]/section/footer/section[2]/button")
    LOCATOR_BLINCHIC = (By.XPATH, "/html/body/div[1]/div[2]/div[1]/div/div[3]/div[3]")
    LOCATOR_COUNT_OF_KIDS = (By.XPATH, "/html/body/div[1]/div[2]/div[1]/div/div[1]/section/div[4]/section[1]/article[2]/fieldset/div/div[3]")
    LOCATOR_KIDS_AGES_FIELD = (By.XPATH, "/html/body/div[1]/div[2]/div[1]/div/div[1]/section/div[4]/section[1]/div/div/fieldset[1]/div/div/div/fieldset/div/input")
    LOCATOR_KIDS_AGES_5 = (By.XPATH, "/html/body/div[1]/div[2]/div[1]/div/div[1]/section/div[4]/section[1]/div/div/fieldset[1]/div/div/div[2]/div/div/div[2]/div/div[7]/div")

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

    def add_kids(self):
        time.sleep(20)
        return self.find_element(SletatSeacrhLocators.LOCATOR_COUNT_OF_KIDS, time=20).click()

    def check_kids_ages_available(self):
        try:
            self.find_element(SletatSeacrhLocators.LOCATOR_KIDS_AGES_FIELD, time=10).click()
            self.find_element(SletatSeacrhLocators.LOCATOR_KIDS_AGES_5, time=10).click()
        except ElementNotInteractableException:
            return False
        return True
