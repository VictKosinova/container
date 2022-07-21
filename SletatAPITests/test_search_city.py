import os
import time
import random
import pytest
import requests
import settings


class TestSecondException(Exception):
    pass


def randomize_town_from():
    countryId = int(settings.get_direction()[0])
    town_from_state = settings.get_direction()[2]
    city_list = []
    for i in town_from_state:
        if i[0] == countryId:
            i = i[1]
            i = int(i)
            city_list.append(i)
    random_city = list(random.choices(city_list, k=3))
    return random_city, countryId


@pytest.mark.parametrize("town_from", randomize_town_from()[0])
class TestRequests:
    def test_compare(self, town_from):
        city_num = 32
        random_country = randomize_town_from()[1]
        url_2 = f"https://module.sletat.ru/slt/Main.svc/GetTours?requestId=0&pageSize=20&pageNumber=1&countryId={random_country}&cityFromId={town_from}&s_nightsMin=6&s_nightsMax=8&currencyAlias=RUB&includeDescriptions=1&includeOilTaxesAndVisa=1&s_showcase=false&filterToursForType=0&s_hotelIsNotInStop=true&s_hasTickets=true&s_ticketsIncluded=false&updateResult=1&visibleOperators={settings.visibleOperators}&s_adults=2&s_departFrom={settings.date_from}&s_departTo={settings.date_to}&calcFullPrice=1&showHotelFacilities=1&requestSource=1"

        req = requests.get(url_2, headers=settings.headers,  proxies=settings.proxies, verify=False)
        result = req.json()['GetToursResult']
        request_id = result['Data']['requestId']
        time.sleep(60)
        req_2 = requests.get(
            F'https://module.sletat.ru/slt/Main.svc/GetTours?requestId={request_id}&pageSize=20&pageNumber=1&countryId={random_country}&cityFromId={town_from}&s_nightsMin=6&s_nightsMax=8&currencyAlias=RUB&includeDescriptions=1&includeOilTaxesAndVisa=1&s_showcase=false&filterToursForType=0&s_hotelIsNotInStop=true&s_hasTickets=true&s_ticketsIncluded=false&updateResult=1&visibleOperators={settings.visibleOperators}&s_adults=2&s_departFrom={settings.date_from}&s_departTo={settings.date_to}&calcFullPrice=1&showHotelFacilities=1&requestSource=1',
            headers=settings.headers, proxies=settings.proxies, verify=False)
        result_2 = req_2.json()
        town_from_result = result_2["GetToursResult"]["Data"]["aaData"]
        if len(town_from_result) != 0:
            for city_info in town_from_result:
                assert town_from_result[0][city_num] == town_from, f"Запрос: {url_2} \nОтвет: {result_2}"
        else:
            print('В ответ на запрос пришел пустой массив')
        print(f'visibleOperators: {settings.visibleOperators} country_id:{random_country} city_from_id:{town_from}')
