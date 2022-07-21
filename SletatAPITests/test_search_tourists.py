import random
import pytest
import requests
import settings
import time


class TestSecondException(Exception):
    pass


def random_tourists():
    z = 0
    tourists_list = []
    while z < 3:
        parameters_list = []
        count_of_adults = random.choice(range(1, 6))
        parameters_list.append(count_of_adults)
        count_of_children = random.choice(range(3))
        parameters_list.append(count_of_children)
        i = 0
        while i < count_of_children:
            age = random.choice(range(13))
            parameters_list.append(age)
            i = i + 1
        z = z + 1
        tourists_list.append(parameters_list)
    return tourists_list


@pytest.mark.parametrize("tourists", random_tourists())
class TestRequests:
    def test_compare(self, tourists):
        adults_num = 16
        kids_num = 17
        countryId = settings.get_direction()[0]
        cityFromId = settings.get_direction()[1]
        adults = tourists[0]
        kids = tourists[1]
        ages_list = []
        for i in tourists:
            if tourists.index(i) >= 2:
                ages_list.append(i)
        if kids == 0:
            ages = ''
        else:
            ages = str(ages_list).replace('[', '').replace(']', '').replace(' ', '')
        url_2 = f"https://module.sletat.ru/slt/Main.svc/GetTours?requestId=0&pageSize=20&pageNumber=1&countryId={countryId}&cityFromId={cityFromId}&s_nightsMin=6&s_nightsMax=8&currencyAlias=RUB&includeDescriptions=1&includeOilTaxesAndVisa=1&s_showcase=false&filterToursForType=0&s_hotelIsNotInStop=true&s_hasTickets=false&s_ticketsIncluded=false&updateResult=1&visibleOperators={settings.visibleOperators}&s_adults={adults}&s_kids={kids}&s_kids_age={ages}&s_departFrom={settings.date_from}&s_departTo={settings.date_to}&calcFullPrice=1&showHotelFacilities=1&requestSource=1"

        req_1 = requests.get(url_2, headers=settings.headers, proxies=settings.proxies, verify=False)
        result_1 = req_1.json()['GetToursResult']
        request_id = result_1['Data']['requestId']
        time.sleep(60)
        req_2 = requests.get(
            F'https://module.sletat.ru/slt/Main.svc/GetTours?requestId={request_id}&pageSize=20&pageNumber=1&countryId={countryId}&cityFromId={cityFromId}&s_nightsMin=6&s_nightsMax=8&currencyAlias=RUB&includeDescriptions=1&includeOilTaxesAndVisa=1&s_showcase=false&filterToursForType=0&s_hotelIsNotInStop=true&s_hasTickets=false&s_ticketsIncluded=false&updateResult=1&visibleOperators={settings.visibleOperators}&s_adults=2&s_departFrom={settings.date_from}&s_departTo={settings.date_to}&calcFullPrice=1&showHotelFacilities=1&requestSource=1',
            headers=settings.headers, proxies=settings.proxies, verify=False)
        result_2 = req_2.json()
        tourists_result = result_2["GetToursResult"]["Data"]["aaData"]
        if len(tourists_result) != 0:
            for tourists_info in tourists_result:
                assert tourists_result[0][adults_num] == adults, f"Запрос: {url_2} \nОтвет: {result_2}"
                assert tourists_result[0][kids_num] == kids, f"Запрос: {url_2} \nОтвет: {result_2}"
        else:
            print('\nВ ответ на запрос пришел пустой массив')
        print(f'visibleOperators: {settings.visibleOperators} country_id:{countryId} city_from_id:{cityFromId} adults: {adults} kids: {kids} kids_ages: {ages}')
