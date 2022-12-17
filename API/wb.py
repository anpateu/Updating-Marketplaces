import requests


class WildberriesAPI:
    def __init__(self, api_key):
        self.headers = {
            "Authorization": str(api_key)
            }

    def get_products(self, skip, take):
        endpoint = f'https://suppliers-api.wildberries.ru/api/v2/stocks?skip={skip}&take={take}'
        response = requests.get(endpoint, headers=self.headers)
        if response.status_code == 200:
            return response.json(), response.json()['total']

    def send_stocks(self, stocks, warehouse):
        endpoint = f"https://suppliers-api.wildberries.ru/api/v3/stocks/{warehouse}"
        body = {"stocks": stocks}
        response = requests.put(endpoint, headers=self.headers, json=body)
        return response.status_code

    def send_prices(self, prices):
        endpoint = "https://suppliers-api.wildberries.ru/public/api/v1/prices"
        response = requests.post(endpoint, headers=self.headers, json=prices)
        if response.status_code == 400:
            return response.json()
        else:
            return response.status_code