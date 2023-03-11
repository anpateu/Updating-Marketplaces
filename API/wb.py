import requests


class WildberriesAPI:
    CARD_LIST_URL = "https://suppliers-api.wildberries.ru/content/v1/cards/cursor/list"
    STOCKS_URL_TEMPLATE = "https://suppliers-api.wildberries.ru/api/v3/stocks/{}"
    PRICES_URL = "https://suppliers-api.wildberries.ru/public/api/v1/prices"

    def __init__(self, api_key):
        self.headers = {"Authorization": str(api_key)}

    def get_cards_data(self):
        nums, codes, barcodes = [], [], []

        data = {
            "sort": {"cursor": {"limit": 1000}, "filter": {"withPhoto": -1}},
        }

        response = requests.post(self.CARD_LIST_URL, headers=self.headers, json=data)
        cards = response.json()

        while True:
            for element in cards["data"]["cards"]:
                nums.append(element.get("nmID"))
                codes.append(element.get("vendorCode"))
                barcodes.append(element["sizes"][0].get("skus", [])[0])

            if len(cards["data"]["cards"]) < 1000:
                break

            last_card = cards["data"]["cards"][-1]
            updatedAt = last_card["updateAt"]
            nmID = last_card["nmID"]

            data["sort"]["cursor"].update({"updatedAt": updatedAt, "nmID": nmID, "limit": 1000})

            response = requests.post(self.CARD_LIST_URL, headers=self.headers, json=data)
            cards = response.json()

        return nums, codes, barcodes

    def send_stocks(self, stocks, warehouse):
        endpoint = self.STOCKS_URL_TEMPLATE.format(warehouse)
        body = {"stocks": stocks}
        response = requests.put(endpoint, headers=self.headers, json=body)
        return response.status_code if response.status_code != 409 else print(response.json())

    def send_prices(self, prices):
        response = requests.post(self.PRICES_URL, headers=self.headers, json=prices)
        return response.status_code