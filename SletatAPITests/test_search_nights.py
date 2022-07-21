import random
import pytest
import requests
import settings
import time


class TestSecondException(Exception):
    pass


def random_nights():
    nights = []
    while len(nights)<3:
        nights_min = random.randint(1, 30)
        nights_max = random.randint(1, 30)
        if abs(nights_max-nights_min) > 9:
            continue
        else:
            if nights_min<nights_max:
                nights.append([nights_min, nights_max])
            else:
                nights.append([nights_max, nights_min])
    return nights


@pytest.mark.parametrize("nights", random_nights())
class TestRequests:
    def test_compare(self, nights):
        nights_num = 14
        countryId = settings.get_direction()[0]
        cityFromId = settings.get_direction()[1]
        nights_min = nights[0]
        nights_max = nights[1]
        url_2 = f"https://module.sletat.ru/slt/Main.svc/GetTours?requestId=0&pageSize=20&pageNumber=1&countryId={countryId}&cityFromId={cityFromId}&s_nightsMin={nights_min}&s_nightsMax={nights_max}&currencyAlias=RUB&includeDescriptions=1&includeOilTaxesAndVisa=1&s_showcase=false&filterToursForType=0&s_hotelIsNotInStop=true&s_hasTickets=false&s_ticketsIncluded=false&updateResult=1&visibleOperators={settings.visibleOperators}&s_adults=2&s_departFrom={settings.date_from}&s_departTo={settings.date_to}&calcFullPrice=1&showHotelFacilities=1&requestSource=1"

        req_1 = requests.get(url_2, headers=settings.headers, proxies=settings.proxies, verify=False)
        result_1 = req_1.json()['GetToursResult']
        request_id = result_1['Data']['requestId']
        time.sleep(60)
        req_2 = requests.get(
            F'https://module.sletat.ru/slt/Main.svc/GetTours?requestId={request_id}&pageSize=20&pageNumber=1&countryId={countryId}&cityFromId={cityFromId}&s_nightsMin={nights_min}&s_nightsMax={nights_max}&currencyAlias=RUB&includeDescriptions=1&includeOilTaxesAndVisa=1&s_showcase=false&filterToursForType=0&s_hotelIsNotInStop=true&s_hasTickets=false&s_ticketsIncluded=false&updateResult=1&visibleOperators={settings.visibleOperators}&s_adults=2&s_departFrom={settings.date_from}&s_departTo={settings.date_to}&calcFullPrice=1&showHotelFacilities=1&requestSource=1',
            headers=settings.headers, proxies=settings.proxies, verify=False)
        result_2 = req_2.json()
        nights_result = result_2["GetToursResult"]["Data"]["aaData"]
        if len(nights_result) != 0:
            for nights_info in nights_result:
                assert nights_result[0][nights_num] in range(nights_min, nights_max), f"Запрос: {url_2} \nОтвет: {result_2}"
        else:
            print('\nВ ответ на запрос пришел пустой массив')
        print(f'visibleOperators: {settings.visibleOperators} country_id:{countryId} city_from_id:{cityFromId} nights_min:{nights_min} nights_max:{nights_max}')