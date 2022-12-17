import requests
import json


class MoySkladAPI:
    def __init__(self, api_key, id_store):
        self.headers = {
            "Authorization": f"Basic {api_key}"
            }
        self.id_store = id_store

    def get_stocks(self, limit, offset):
        store = f"https://online.moysklad.ru/api/remap/1.2/entity/store/{self.id_store}"
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