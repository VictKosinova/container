import time
import random
import pytest
import requests
import settings


class TestSecondException(Exception):
    pass


def randomize_country():
    cityFromId = int(settings.get_direction()[1])
    town_from_state = settings.get_direction()[2]
    country_list = []
    for i in town_from_state:
        if i[1] == cityFromId:
            i = i[0]
            i = int(i)
            country_list.append(i)
    random_country = list(random.choices(country_list, k=3))
    return random_country, cityFromId


@pytest.mark.parametrize("country", randomize_country()[0])
class TestRequests:
    def test_compare(self, country):
        country_num = 30
        random_city = randomize_country()[1]
        url_2 = f"https://module.sletat.ru/slt/Main.svc/GetTours?requestId=0&pageSize=20&pageNumber=1&countryId={country}&cityFromId={random_city}&s_nightsMin=6&s_nightsMax=8&currencyAlias=RUB&includeDescriptions=1&includeOilTaxesAndVisa=1&s_showcase=false&filterToursForType=0&s_hotelIsNotInStop=true&s_hasTickets=true&s_ticketsIncluded=false&updateResult=1&visibleOperators={settings.visibleOperators}&s_adults=2&s_departFrom={settings.date_from}&s_departTo={settings.date_to}&calcFullPrice=1&showHotelFacilities=1&requestSource=1"
        req = requests.get(url_2, headers=settings.headers, proxies=settings.proxies, verify=False)
        result = req.json()['GetToursResult']
        request_id = result['Data']['requestId']
        time.sleep(60)
        req_2 = requests.get(
            F'https://module.sletat.ru/slt/Main.svc/GetTours?requestId={request_id}&pageSize=20&pageNumber=1&countryId={country}&cityFromId={random_city}&s_nightsMin=6&s_nightsMax=8&currencyAlias=RUB&includeDescriptions=1&includeOilTaxesAndVisa=1&s_showcase=false&filterToursForType=0&s_hotelIsNotInStop=true&s_hasTickets=true&s_ticketsIncluded=false&updateResult=1&visibleOperators={settings.visibleOperators}&s_adults=2&s_departFrom={settings.date_from}&s_departTo={settings.date_to}&calcFullPrice=1&showHotelFacilities=1&requestSource=1',
            headers=settings.headers, proxies=settings.proxies, verify=False)
        result_2 = req_2.json()
        country_result = result_2["GetToursResult"]["Data"]["aaData"]
        if len(country_result) != 0:
            for country_info in country_result:
                assert country_result[0][country_num] == country, f"Запрос: {url_2} \nОтвет: {result_2}"
        else:
            print('В ответ на запрос пришел пустой массив')
        print(f'visibleOperators: {settings.visibleOperators} country_id:{country} city_from_id:{random_city}')
