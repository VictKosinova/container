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
    LOCATOR_KIDS_AGES_FIELD_1 = (By.XPATH, "/html/body/div[1]/div[2]/div[1]/div/div[1]/section/div[4]/section[1]/div/div/fieldset[1]/div/div/div/fieldset/div/input")
    LOCATOR_KIDS_AGES_1_5 = (By.XPATH, "/html/body/div[1]/div[2]/div[1]/div/div[1]/section/div[4]/section[1]/div/div/fieldset[1]/div/div/div[2]/div/div/div[2]/div/div[7]/div")
    LOCATOR_HOTEL_CATEGORY_3 = (By.XPATH, "/html/body/div[2]/div[2]/div[1]/div/div[1]/section/div[2]/div[2]/div[2]/div/button[1]")
    LOCATOR_ALL_CATEGORIES = (By.XPATH, "/html/body/div[2]/div[2]/div[1]/div/div[1]/section/div[2]/div[2]")
    LOCATOR_HEADER_OF_3_HOTELS = (By.XPATH, "/html/body/div[2]/div[2]/div[1]/div/div[1]/section/div[3]/section[2]/fieldset/div/div[2]/li/span/span")

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
            return True

    def add_kids(self):
        time.sleep(20)
        return self.find_element(SletatSeacrhLocators.LOCATOR_COUNT_OF_KIDS, time=20).click()

    def check_kids_ages_available(self):
        try:
            self.find_element(SletatSeacrhLocators.LOCATOR_KIDS_AGES_FIELD_1, time=10).click()
            self.find_element(SletatSeacrhLocators.LOCATOR_KIDS_AGES_1_5, time=10).click()
        except ElementNotInteractableException:
            return False
        return True

    def choose_hotel_category(self):
        return self.find_element(SletatSeacrhLocators.LOCATOR_HOTEL_CATEGORY_3, time=20).click()

    def all_categories_field_is_selected(self):
        return self.find_element(SletatSeacrhLocators.LOCATOR_ALL_CATEGORIES, time=10).is_selected()

    def check_header_of_hotels_right(self):
        try:
            self.find_element(SletatSeacrhLocators.LOCATOR_HEADER_OF_3_HOTELS, time=10).click()
        except NoSuchElementException:
            return False
        return True
