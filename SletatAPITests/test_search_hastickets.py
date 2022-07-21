import time
import requests
import settings


class TestSecondException(Exception):
    pass


class TestRequests:
    def test_compare(self):
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
        tickets_result = result_2["GetToursResult"]["Data"]["aaData"]
        if len(tickets_result) != 0:
            for tickets_info in tickets_result:
                tickets_list = []
                economic_tickets = tickets_result[0][23]
                tickets_list.append(economic_tickets)
                economic_tickets_back = tickets_result[0][24]
                tickets_list.append(economic_tickets_back)
                business_tickets = tickets_result[0][25]
                tickets_list.append(business_tickets)
                business_tickets_back = tickets_result[0][26]
                tickets_list.append(business_tickets_back)
                for i in tickets_list:
                    assert int(i) in [0, 1], f"Запрос: {url_2} \nОтвет: {result_2}"
        else:
            print('В ответ на запрос пришел пустой массив')
        print(f'visibleOperators: {settings.visibleOperators} country_id:{countryId} city_from_id:{cityFromId}')

