import time
import random
import pytest
import requests
import settings
import socket

socket = socket.socket()

class TestSecondException(Exception):
    pass


def randomize_resort():
    resorts_state_list = settings.get_resorts()
    resorts_list = [i[0] for i in resorts_state_list]
    random_resort = [random.choices(resorts_list, k=3),random.choices(resorts_list, k=3),random.choices(resorts_list, k=3)]
    return random_resort


@pytest.mark.parametrize("resorts", randomize_resort())
class TestRequests:
    def test_compare(self, resorts):
        resort_num = 5
        countryId = settings.get_direction()[0]
        cityFromId = settings.get_direction()[1]
        resorts_collection = str(resorts).replace(' ', '')
        url_2 = f"https://module.sletat.ru/slt/Main.svc/GetTours?requestId=0&pageSize=20&pageNumber=1&countryId={countryId}&cityFromId={cityFromId}&resort={resorts_collection}&s_nightsMin=6&s_nightsMax=8&currencyAlias=RUB&includeDescriptions=1&includeOilTaxesAndVisa=1&s_showcase=false&filterToursForType=0&s_hotelIsNotInStop=true&s_hasTickets=true&s_ticketsIncluded=false&updateResult=1&visibleOperators={settings.visibleOperators}&s_adults=2&s_departFrom={settings.date_from}&s_departTo={settings.date_to}&calcFullPrice=1&showHotelFacilities=1&requestSource=1"

        req = requests.get(url_2, headers=settings.headers, proxies=settings.proxies, verify=False)
        result = req.json()['GetToursResult']
        request_id = result['Data']['requestId']
        time.sleep(60)
        req_2 = requests.get(
            F'https://module.sletat.ru/slt/Main.svc/GetTours?requestId={request_id}&pageSize=20&pageNumber=1&countryId={countryId}&cityFromId={cityFromId}&resort={resorts_collection}&s_nightsMin=6&s_nightsMax=8&currencyAlias=RUB&includeDescriptions=1&includeOilTaxesAndVisa=1&s_showcase=false&filterToursForType=0&s_hotelIsNotInStop=true&s_hasTickets=true&s_ticketsIncluded=false&updateResult=1&visibleOperators={settings.visibleOperators}&s_adults=2&s_departFrom={settings.date_from}&s_departTo={settings.date_to}&calcFullPrice=1&showHotelFacilities=1&requestSource=1',
            headers=settings.headers, proxies=settings.proxies, verify=False)
        result_2 = req_2.json()
        resorts_result = result_2["GetToursResult"]["Data"]["aaData"]
        if len(resorts_result) != 0:
            for resort_info in resorts_result:
                assert resorts_result[0][resort_num] in resorts, f"Запрос: {url_2} \nОтвет: {result_2}"
        else:
            print('В ответ на запрос пришел пустой массив')
        print(f'visibleOperators: {settings.visibleOperators} country_id:{countryId} city_from_id:{cityFromId} resorts:{resorts}')
