import random
import sys
import time
import pytest
import requests
import settings
import urllib3
import certifi

http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where()
)


countryId = int(settings.get_direction()[0])
cityFromId = int(settings.get_direction()[1])


class TestSecondException(Exception):
    pass


def _get_request_id():
    url = f"https://module.sletat.ru/slt/Main.svc/GetTours?requestId=0&pageSize=20&pageNumber=1&countryId={countryId}&cityFromId={cityFromId}&s_nightsMin=6&s_nightsMax=8&currencyAlias=RUB&includeDescriptions=1&includeOilTaxesAndVisa=1&s_showcase=false&filterToursForType=0&s_hotelIsNotInStop=true&s_hasTickets=true&s_ticketsIncluded=false&updateResult=1&visibleOperators={settings.visibleOperators}&s_adults=2&s_departFrom={settings.date_from}&s_departTo={settings.date_to}&calcFullPrice=1&showHotelFacilities=1&requestSource=1"
    try:
        req = requests.get(url, proxies=settings.proxies, headers=settings.headers, verify=False)
        result = req.json()['GetToursResult']
    except requests.exceptions.RequestException as e:
        sys.stderr.write(f'Error response')
        raise
    if result['ErrorMessage']:
        raise TestSecondException(result['ErrorMessage'])
    return result['Data']['requestId']


def request_prices_all():
    req_id = _get_request_id()
    time.sleep(20)
    res = requests.get(
        f'https://module.sletat.ru/slt/Main.svc/GetTours?requestId={req_id}&pageSize=20&pageNumber=1&countryId={countryId}&cityFromId={cityFromId}&s_nightsMin=6&s_nightsMax=8&currencyAlias=RUB&includeDescriptions=1&includeOilTaxesAndVisa=1&s_showcase=false&filterToursForType=0&s_hotelIsNotInStop=true&s_hasTickets=true&s_ticketsIncluded=false&updateResult=1&visibleOperators={settings.visibleOperators}&s_adults=2&s_departFrom={settings.date_from}&s_departTo={settings.date_to}&calcFullPrice=1&showHotelFacilities=1&requestSource=1',
        headers=settings.headers, proxies=settings.proxies, verify=False)
    result = res.json()
    aa_data = result["GetToursResult"]["Data"]["aaData"]
    if len(aa_data) == 0:
        print('В ответ на запрос пришел пустой массив')
    else:
        prices_list = []
        i = 0
        while i < 3:
            prices = {i[42] for i in aa_data}
            all_prices_list = list(prices)
            random_prices = random.choices(all_prices_list, k=2)
            if random_prices[0] > random_prices[1]:
                max_price = random_prices[0]
                min_price = random_prices[1]
            else:
                max_price = random_prices[1]
                min_price = random_prices[0]
            if len(all_prices_list) > 1 and min_price == max_price:
                continue
            else:
                prices_list.append([min_price, max_price])
                i = 1 + i
        return prices_list


@pytest.mark.parametrize("prices", request_prices_all())
class TestRequests:
    def test_compare(self, prices):
        prices_num = 42
        min_price = prices[0]
        max_price = prices[1]
        time.sleep(60)
        url_2 = f"https://module.sletat.ru/slt/Main.svc/GetTours?requestId=0&pageSize=20&pageNumber=1&countryId={countryId}&cityFromId={cityFromId}&s_priceMin={min_price}&s_priceMax={max_price}&s_nightsMin=6&s_nightsMax=6&currencyAlias=RUB&includeDescriptions=1&includeOilTaxesAndVisa=1&minHotelRating=0&s_showcase=false&filterToursForType=0&s_hotelIsNotInStop=true&s_hasTickets=true&s_ticketsIncluded=false&updateResult=1&visibleOperators={settings.visibleOperators}&s_adults=2&s_departFrom={settings.date_from}&s_departTo={settings.date_to}&calcFullPrice=1&showHotelFacilities=1&requestSource=1"
        try:
            req_2 = requests.get(url_2, headers=settings.headers, proxies=settings.proxies, verify=False)
            result_2 = req_2.json()['GetToursResult']
        except requests.exceptions.RequestException as e:
            sys.stderr.write('Error response')
            raise
        if result_2['ErrorMessage']:
            raise TestSecondException(result_2['ErrorMessage'])
        request_id_2 = result_2['Data']['requestId']
        time.sleep(60)
        part_req = requests.get(
            F'https://module.sletat.ru/slt/Main.svc/GetTours?requestId={request_id_2}&pageSize=20&pageNumber=1&countryId={countryId}&cityFromId={cityFromId}&s_priceMin={min_price}&s_priceMax={max_price}&s_nightsMin=6&s_nightsMax=6&currencyAlias=RUB&includeDescriptions=1&includeOilTaxesAndVisa=1&minHotelRating=0&s_showcase=false&filterToursForType=0&s_hotelIsNotInStop=true&s_hasTickets=true&s_ticketsIncluded=false&updateResult=1&visibleOperators={settings.visibleOperators}&s_adults=2&s_departFrom={settings.date_from}&s_departTo={settings.date_to}&calcFullPrice=1&showHotelFacilities=1&requestSource=1',
            headers=settings.headers, proxies=settings.proxies, verify=False)
        result_3 = part_req.json()
        prices_result = result_3["GetToursResult"]["Data"]["aaData"]
        if len(prices_result) != 0:
            for prices_info in prices_result:
                assert prices_result[0][prices_num] >= min_price and prices_result[0][prices_num] <= max_price, f"Запрос: {url_2} \nОтвет: {result_3}"
        else:
            print('В ответ на запрос пришел пустой массив')
        print(f'visibleOperators: {settings.visibleOperators} country_id:{countryId} city_from_id:{cityFromId} min_price: {min_price} max_price: {max_price}')