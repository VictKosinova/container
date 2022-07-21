import sys
import time
import random
import pytest
import requests
import settings

countryId = settings.get_direction()[0]
cityFromId = settings.get_direction()[1]


class TestSecondException(Exception):
    pass


def _get_request_id():
    url = f"https://module.sletat.ru/slt/Main.svc/GetTours?requestId=0&pageSize=20&pageNumber=1&countryId={countryId}&cityFromId={cityFromId}&s_nightsMin=6&s_nightsMax=8&currencyAlias=RUB&includeDescriptions=1&includeOilTaxesAndVisa=1&s_showcase=false&filterToursForType=0&s_hotelIsNotInStop=true&s_hasTickets=true&s_ticketsIncluded=false&updateResult=1&visibleOperators={settings.visibleOperators}&s_adults=2&s_departFrom={settings.date_from}&s_departTo={settings.date_to}&calcFullPrice=1&showHotelFacilities=1&requestSource=1"

    try:
        req = requests.get(url, proxies=settings.proxies, headers=settings.headers, verify=False)
        result = req.json()['GetToursResult']
    except requests.exceptions.RequestException as e:
        sys.stderr.write('invalid request')
        raise

    if result['ErrorMessage']:
        raise TestSecondException(result['ErrorMessage'])

    return result['Data']['requestId']


def request_hotels_all():
    req_id = _get_request_id()
    time.sleep(20)
    res = requests.get(
        f'https://module.sletat.ru/slt/Main.svc/GetTours?requestId={req_id}&pageSize=20&pageNumber=1&countryId={countryId}&cityFromId={cityFromId}&s_nightsMin=6&s_nightsMax=8&currencyAlias=RUB&includeDescriptions=1&includeOilTaxesAndVisa=1&s_showcase=false&filterToursForType=0&s_hotelIsNotInStop=true&s_hasTickets=true&s_ticketsIncluded=false&updateResult=1&visibleOperators={settings.visibleOperators}&s_adults=2&s_departFrom={settings.date_from}&s_departTo={settings.date_to}&calcFullPrice=1&showHotelFacilities=1&requestSource=1',
        headers=settings.headers, proxies=settings.proxies, verify=False)

    result = res.json()

    aa_data = result["GetToursResult"]["Data"]["aaData"]
    if len(aa_data) != 0:
        hotel_ids_set = {arr[3] for arr in aa_data}
        hotel_ids_list = list(hotel_ids_set)
        hotel_ids = random.choices(hotel_ids_list, k=3)
        return hotel_ids
    else:
        print('В ответ на запрос пришел пустой массив')


@pytest.mark.parametrize("hotel_id", request_hotels_all())
class TestRequests:
    _hotel_id_num = 3
    def test_compare(self, hotel_id):
        time.sleep(60)
        url_2 = f"https://module.sletat.ru/slt/Main.svc/GetTours?requestId=0&pageSize=20&pageNumber=1&countryId={countryId}&cityFromId={cityFromId}&hotels={hotel_id}&s_nightsMin=6&s_nightsMax=8&currencyAlias=RUB&includeDescriptions=1&includeOilTaxesAndVisa=1&s_showcase=false&filterToursForType=0&s_hotelIsNotInStop=true&s_hasTickets=true&s_ticketsIncluded=false&updateResult=1&visibleOperators={settings.visibleOperators}&s_adults=2&s_departFrom={settings.date_from}&s_departTo={settings.date_to}&calcFullPrice=1&showHotelFacilities=1&requestSource=1"
        try:
            req_2 = requests.get(url_2, headers=settings.headers, proxies=settings.proxies, verify=False)
            result_2 = req_2.json()['GetToursResult']
        except requests.exceptions.RequestException as e:
            sys.stderr.write('invalid request')
            raise

        if result_2['ErrorMessage']:
            raise TestSecondException(result_2['ErrorMessage'])
        request_id_2 = result_2['Data']['requestId']
        time.sleep(60)
        part_req = requests.get(
            F'https://module.sletat.ru/slt/Main.svc/GetTours?requestId={request_id_2}&pageSize=20&pageNumber=1&countryId={countryId}&cityFromId={cityFromId}&hotels={hotel_id}&s_nightsMin=6&s_nightsMax=8&currencyAlias=RUB&includeDescriptions=1&includeOilTaxesAndVisa=1&s_showcase=false&filterToursForType=0&s_hotelIsNotInStop=true&s_hasTickets=true&s_ticketsIncluded=false&updateResult=1&visibleOperators={settings.visibleOperators}&s_adults=2&s_departFrom={settings.date_from}&s_departTo={settings.date_to}&calcFullPrice=1&showHotelFacilities=1&requestSource=1',
            headers=settings.headers, proxies=settings.proxies, verify=False)
        result_3 = part_req.json()
        hotels_result = result_3["GetToursResult"]["Data"]["aaData"]
        if len(hotels_result) != 0:
            for hotel_info in hotels_result:
                assert hotels_result[0][self._hotel_id_num] == hotel_id, f"Запрос: {url_2} \nОтвет: {result_3}"
        else:
            print('В ответ на запрос пришел пустой массив')
        print(f'visibleOperators: {settings.visibleOperators} country_id:{countryId} city_from_id:{cityFromId} hotelId:{hotel_id}')
