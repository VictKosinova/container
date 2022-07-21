import random
import pytest
import requests
import settings
import time


class TestSecondException(Exception):
    pass


def random_meal():
    req = requests.get("https://module.sletat.ru/Main.svc/GetMeals", headers=settings.headers, proxies=settings.proxies, verify=False)
    result = req.json()['GetMealsResult']['Data']
    meals = random.choices(result, k=3)
    return meals


@pytest.mark.parametrize("meal", random_meal())
class TestRequests:
    def test_compare(self, meal):
        meals_num = 10
        countryId = settings.get_direction()[0]
        cityFromId = settings.get_direction()[1]
        meal_id = meal['Id']
        url_2 = f"https://module.sletat.ru/slt/Main.svc/GetTours?requestId=0&pageSize=20&pageNumber=1&countryId={countryId}&cityFromId={cityFromId}&meals={meal_id}&s_nightsMin=6&s_nightsMax=8&currencyAlias=RUB&includeDescriptions=1&includeOilTaxesAndVisa=1&s_showcase=false&filterToursForType=0&s_hotelIsNotInStop=true&s_hasTickets=false&s_ticketsIncluded=false&updateResult=1&visibleOperators={settings.visibleOperators}&s_adults=2&s_departFrom={settings.date_from}&s_departTo={settings.date_to}&calcFullPrice=1&showHotelFacilities=1&requestSource=1"

        req_1 = requests.get(url_2, headers=settings.headers, proxies=settings.proxies, verify=False)
        result_1 = req_1.json()['GetToursResult']
        request_id = result_1['Data']['requestId']
        time.sleep(60)
        req_2 = requests.get(
            F'https://module.sletat.ru/slt/Main.svc/GetTours?requestId={request_id}&pageSize=20&pageNumber=1&countryId={countryId}&cityFromId={cityFromId}&meals={meal_id}&s_nightsMin=6&s_nightsMax=8&currencyAlias=RUB&includeDescriptions=1&includeOilTaxesAndVisa=1&s_showcase=false&filterToursForType=0&s_hotelIsNotInStop=true&s_hasTickets=false&s_ticketsIncluded=false&updateResult=1&visibleOperators={settings.visibleOperators}&s_adults=2&s_departFrom={settings.date_from}&s_departTo={settings.date_to}&calcFullPrice=1&showHotelFacilities=1&requestSource=1',
            headers=settings.headers, proxies=settings.proxies, verify=False)
        result_2 = req_2.json()
        meals_result = result_2["GetToursResult"]["Data"]["aaData"]
        if len(meals_result) != 0:
            for meals_info in meals_result:
                assert meals_result[0][meals_num] == meal["Name"], f"Запрос: {url_2} \nОтвет: {result_2}"
        else:
            print('\nВ ответ на запрос пришел пустой массив')
        print(f'visibleOperators: {settings.visibleOperators} country_id:{countryId} city_from_id:{cityFromId} mealId:{meal}')
