import time
import random
import pytest
import requests
import settings


class TestSecondException(Exception):
    pass


def randomize_stars():
    stars = (401, 402, 403, 404, 405, 410, 411)
    random_stars_set = [random.choices(stars, k=3), random.choices(stars, k=3), random.choices(stars, k=3)]
    return random_stars_set


@pytest.mark.parametrize("star", randomize_stars())
class TestRequests:
    def test_compare(self, star):
        stars_num = 8
        countryId = settings.get_direction()[0]
        cityFromId = settings.get_direction()[1]
        url_2 = f"https://module.sletat.ru/slt/Main.svc/GetTours?requestId=0&pageSize=20&pageNumber=1&countryId={countryId}&cityFromId={cityFromId}&stars={str(star)[1:-1]}&s_nightsMin=6&s_nightsMax=8&currencyAlias=RUB&includeDescriptions=1&includeOilTaxesAndVisa=1&s_showcase=false&filterToursForType=0&s_hotelIsNotInStop=true&s_hasTickets=true&s_ticketsIncluded=false&updateResult=1&visibleOperators={settings.visibleOperators}&s_adults=2&s_departFrom={settings.date_from}&s_departTo={settings.date_to}&calcFullPrice=1&showHotelFacilities=1&requestSource=1"

        req = requests.get(url_2, headers=settings.headers, proxies=settings.proxies, verify=False)
        result = req.json()['GetToursResult']
        request_id = result['Data']['requestId']
        time.sleep(60)
        req_2 = requests.get(
            F'https://module.sletat.ru/slt/Main.svc/GetTours?requestId={request_id}&pageSize=20&pageNumber=1&countryId={countryId}&cityFromId={cityFromId}&stars={str(star)[1:-1]}&s_nightsMin=6&s_nightsMax=8&currencyAlias=RUB&includeDescriptions=1&includeOilTaxesAndVisa=1&s_showcase=false&filterToursForType=0&s_hotelIsNotInStop=true&s_hasTickets=true&s_ticketsIncluded=false&updateResult=1&visibleOperators={settings.visibleOperators}&s_adults=2&s_departFrom={settings.date_from}&s_departTo={settings.date_to}&calcFullPrice=1&showHotelFacilities=1&requestSource=1',
            headers=settings.headers, proxies=settings.proxies, verify=False)
        result_2 = req_2.json()
        stars_result = result_2["GetToursResult"]["Data"]["aaData"]
        if len(stars_result) != 0:
            stars_2 = {401: '2*', 402: '3*', 403: '4*', 404: '5*', 405: 'Apts', 410: 'HV-1', 411: 'HV-2'}
            stars_set_2 = [stars_2[a] for a in star]
            for stars_info in stars_result:
                assert stars_result[0][stars_num] in stars_set_2, f"Запрос: {url_2} \nОтвет: {result_2}"
        else:
            print('В ответ на запрос пришел пустой массив')
        print(f'visibleOperators: {settings.visibleOperators} country_id:{countryId} city_from_id:{cityFromId} stars:{str(star)[1:-1]}')