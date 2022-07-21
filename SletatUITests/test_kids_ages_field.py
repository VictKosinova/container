from SletatPages import SearchHelper


def test_field_available(browser):
    sletat_main_page = SearchHelper(browser)
    sletat_main_page.go_to_site()
    sletat_main_page.add_kids()
    is_available = sletat_main_page.check_kids_ages_available()
    assert is_available is True, "The item is unavailable"
