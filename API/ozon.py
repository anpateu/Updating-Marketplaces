import requests
import json


class OzonAPI:
    def __init__(self, api_key, client_id):
        self.headers = {
            "Client-Id": str(client_id),
            "Api-Key": str(api_key)
            }

    def check_ok(self, response):
        if response.status_code == 200:
            return response.reason
        else:
            return response.text

    def get_products(self, limit, last_id):
        endpoint = "https://api-seller.ozon.ru/v2/product/list"
        body = {
            "last_id": last_id,
            "limit": limit
            }
        response = requests.post(endpoint, headers=self.headers, data=json.dumps(body))
        return response.json()

    def send_stocks(self, stocks):
        endpoint = "https://api-seller.ozon.ru/v2/products/stocks"
        body = {"stocks": stocks}
        response = requests.post(endpoint, headers=self.headers, data=json.dumps(body))
        return self.check_ok(response)

    def send_prices(self, prices):
        endpoint = "https://api-seller.ozon.ru/v1/product/import/prices"
        body = {"prices": prices}
        response = requests.post(endpoint, headers=self.headers, data=json.dumps(body))
        return self.check_ok(response)