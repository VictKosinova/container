import random
import pytest
import requests
import settings
import time


class TestSecondException(Exception):
    pass


def random_rating():
    rating_list = [0, 6, 7, 8, 9]
    rating = random.choices(rating_list, k=3)
    return rating


@pytest.mark.parametrize("rating", random_rating())
class TestRequests:
    def test_compare(self, rating):
        rating_num = 35
        countryId = settings.get_direction()[0]
        cityFromId = settings.get_direction()[1]
        url_2 = f"https://module.sletat.ru/slt/Main.svc/GetTours?requestId=0&pageSize=20&pageNumber=1&countryId={countryId}&cityFromId={cityFromId}&minHotelRating={rating}&s_nightsMin=6&s_nightsMax=8&currencyAlias=RUB&includeDescriptions=1&includeOilTaxesAndVisa=1&s_showcase=false&filterToursForType=0&s_hotelIsNotInStop=true&s_hasTickets=false&s_ticketsIncluded=false&updateResult=1&visibleOperators={settings.visibleOperators}&s_adults=2&s_departFrom={settings.date_from}&s_departTo={settings.date_to}&calcFullPrice=1&showHotelFacilities=1&requestSource=1"

        req_1 = requests.get(url_2, headers=settings.headers, proxies=settings.proxies, verify=False)
        result_1 = req_1.json()['GetToursResult']
        request_id = result_1['Data']['requestId']
        time.sleep(80)
        req_2 = requests.get(
            F'https://module.sletat.ru/slt/Main.svc/GetTours?requestId={request_id}&pageSize=20&pageNumber=1&countryId={countryId}&cityFromId={cityFromId}&minHotelRating={rating}&s_nightsMin=6&s_nightsMax=8&currencyAlias=RUB&includeDescriptions=1&includeOilTaxesAndVisa=1&s_showcase=false&filterToursForType=0&s_hotelIsNotInStop=true&s_hasTickets=false&s_ticketsIncluded=false&updateResult=1&visibleOperators={settings.visibleOperators}&s_adults=2&s_departFrom={settings.date_from}&s_departTo={settings.date_to}&calcFullPrice=1&showHotelFacilities=1&requestSource=1',
            headers=settings.headers, proxies=settings.proxies, verify=False)
        result_2 = req_2.json()
        rating_result = result_2["GetToursResult"]["Data"]["aaData"]
        if len(rating_result) != 0:
            for meals_info in rating_result:
                assert float(rating_result[0][rating_num]) >= float(rating), f"Запрос: {url_2} \nОтвет: {result_2}"
        else:
            print('\nВ ответ на запрос пришел пустой массив')
        print(f'visibleOperators: {settings.visibleOperators} country_id:{countryId} city_from_id:{cityFromId} rating:{rating}')
