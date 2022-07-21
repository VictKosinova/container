import time
import requests
import settings


class TestSecondException(Exception):
    pass


class TestRequests:
    def test_compare(self):
        places_num = 21
        countryId = settings.get_direction()[0]
        cityFromId = settings.get_direction()[1]
        url_2 = f"https://module.sletat.ru/slt/Main.svc/GetTours?requestId=0&pageSize=20&pageNumber=1&countryId={countryId}&cityFromId={cityFromId}&s_nightsMin=6&s_nightsMax=8&currencyAlias=RUB&includeDescriptions=1&includeOilTaxesAndVisa=1&s_showcase=false&filterToursForType=0&s_hotelIsNotInStop=true&s_hasTickets=true&s_ticketsIncluded=true&updateResult=1&visibleOperators={settings.visibleOperators}&s_adults=2&s_departFrom={settings.date_from}&s_departTo={settings.date_to}&calcFullPrice=1&showHotelFacilities=1&requestSource=1"

        req = requests.get(url_2, headers=settings.headers, proxies=settings.proxies, verify=False)
        result = req.json()['GetToursResult']
        request_id = result['Data']['requestId']
        time.sleep(60)
        req_2 = requests.get(
            F'https://module.sletat.ru/slt/Main.svc/GetTours?requestId={request_id}&pageSize=20&pageNumber=1&countryId={countryId}&cityFromId={cityFromId}&s_nightsMin=6&s_nightsMax=8&currencyAlias=RUB&includeDescriptions=1&includeOilTaxesAndVisa=1&s_showcase=false&filterToursForType=0&s_hotelIsNotInStop=true&s_hasTickets=true&s_ticketsIncluded=true&updateResult=1&visibleOperators={settings.visibleOperators}&s_adults=2&s_departFrom={settings.date_from}&s_departTo={settings.date_to}&calcFullPrice=1&showHotelFacilities=1&requestSource=1',
            headers=settings.headers, proxies=settings.proxies, verify=False)
        result_2 = req_2.json()
        places_result = result_2["GetToursResult"]["Data"]["aaData"]
        if len(places_result) != 0:
            assert int(places_result[0][places_num]) in [0, 2], f"Запрос: {url_2} \nОтвет: {result_2}"
        else:
            print('В ответ на запрос пришел пустой массив')
        print(f'visibleOperators: {settings.visibleOperators} country_id:{countryId} city_from_id:{cityFromId}')
