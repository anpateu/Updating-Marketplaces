import requests
import json


class MoySkladAPI:
    def __init__(self, api_key):
        self.headers = {
            "Authorization": f"Basic {api_key}"
            }

    def get_stocks(self, store_id, limit, offset):
        store = f"https://online.moysklad.ru/api/remap/1.2/entity/store/{store_id}"
        endpoint = (
            "https://online.moysklad.ru/api/remap/1.2/report/stock/all?"
            "quantityMode=positiveOnly&"
            "filter=store={store}&"
            "limit={limit}&"
            "offset={offset}"
        )
        endpoint = endpoint.format(store=store, limit=limit, offset=offset)
        response = requests.get(endpoint, headers=self.headers, data=json.dumps({}))
        return response.json()