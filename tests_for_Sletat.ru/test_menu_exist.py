from SletatPages import SearchHelper


def test_menu_exist(browser):
    sletat_main_page = SearchHelper(browser)
    sletat_main_page.go_to_site()
    sletat_main_page.enter_word("Франция")
    sletat_main_page.click_on_the_search_button()
    elements = sletat_main_page.check_blinchik_exist()
    assert elements == "Exist"
