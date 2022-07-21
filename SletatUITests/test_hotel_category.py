from SletatPages import SearchHelper


def test_checking_all_categories_field(browser):
    sletat_main_page = SearchHelper(browser)
    sletat_main_page.go_to_site()
    sletat_main_page.choose_hotel_category()
    is_selected = sletat_main_page.all_categories_field_is_selected()
    is_header_right = sletat_main_page.check_header_of_hotels_right()
    assert is_selected is False and is_header_right is True, "Field slected"
    # assert is_header_right is True, "Header isn't right"
