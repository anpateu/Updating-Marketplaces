import requests
import json


class MoySkladAPI:
    def __init__(self, api_key):
        self.headers = {
            "Authorization": f"Basic {api_key}"
            }
        self.attribute_id = "71723415-3d69-11ed-0a80-0e670029ce8e"

    def get_stocks(self, store_id, limit, offset):
        store = f"https://online.moysklad.ru/api/remap/1.2/entity/store/{store_id}"
        endpoint = (
            "https://online.moysklad.ru/api/remap/1.2/report/stock/all?"
            "filter=store={store};quantityMode=positiveonly&"
            "limit={limit}&"
            "offset={offset}"
        )
        endpoint = endpoint.format(store=store, limit=limit, offset=offset)
        response = requests.get(endpoint, headers=self.headers, data=json.dumps({}))
        return response.json()

    def get_all_products(self, stores, limit, offset):
        endpoint = (
            "https://online.moysklad.ru/api/remap/1.2/report/stock/all?"
            "filter={filter};stockMode=positiveonly;quantityMode=all&"
            "limit={limit}&"
            "offset={offset}"
        )
        filter = ""
        for store_id in stores:
            filter += f"store=https://online.moysklad.ru/api/remap/1.2/entity/store/{store_id};"
        endpoint = endpoint.format(filter=filter, limit=limit, offset=offset)
        response = requests.get(endpoint, headers=self.headers, data=json.dumps({}))
        return response.json()

    def get_product(self, product_id):
        endpoint = f"https://online.moysklad.ru/api/remap/1.2/entity/product/{product_id}"
        response = requests.get(endpoint, headers=self.headers)
        return response.json()

    def get_entity(self, entity):
        response = requests.get(entity, headers=self.headers)
        return response.json()

    def update_price(self, meta, price, price_name):
        endpoint = f"https://online.moysklad.ru/api/remap/1.1/entity/product/{meta}"
        body = {
            "salePrices": [{
                "value": int(price) * 100,
                "priceType": price_name
                }]
            }
        response = requests.put(endpoint, headers=self.headers, json=body)
        return response.json()

    def get_extra_info(self):
        attribute = f"https://online.moysklad.ru/api/remap/1.2/entity/product/metadata/attributes/{self.attribute_id}"
        endpoint = f"https://online.moysklad.ru/api/remap/1.2/report/stock/all?filter={attribute}!="
        response = requests.get(endpoint, headers=self.headers)
        return response.json()

    def update_product(self, data):
        endpoint = "https://online.moysklad.ru/api/remap/1.2/entity/product"
        response = requests.post(endpoint, headers=self.headers, json=data)
        return response.json()