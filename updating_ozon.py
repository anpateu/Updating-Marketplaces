import shelve
import math
from config import Config
from API.ozon import OzonAPI


def load_products(total, last_id):
    total = math.ceil(total / 1000)
    codes, ids = [], []
    for i in range(total):
        data = api.get_products(1000, last_id)
        last_id = data['result']['last_id']
        for element in data['result']['items']:
            codes.append(element['offer_id'])
            ids.append(element['product_id'])
    return codes, ids

def updating_ozon(api, warehouse_id):
    total = api.get_products(1, "")['result']['total']
    codes, ids = load_products(total, "")
    body_stocks, body_prices = [], []

    for i in range(len(codes)):
        product_id = ids[i]
        offer_id = codes[i]
        with shelve.open('data/stocks') as data:
            stocks = data.get(offer_id, 0)
        with shelve.open('data/prices') as data:
            price = data.get(offer_id, 0)

        product_stocks = {
            "offer_id": str(offer_id),
            "product_id": int(product_id),
            "stock": int(stocks),
            "warehouse_id": int(warehouse_id)
            }
        body_stocks.append(product_stocks)

        if price > 0:
            product_prices = {
                "auto_action_enabled": "UNKNOWN",
                "min_price": str(int(float(price)*0.95)),
                "offer_id": str(offer_id),
                "old_price": str(int(float(price)*1.44)),
                "price": str(price),
                "product_id": int(product_id)
                }
            body_prices.append(product_prices)

    for i in range(0, len(body_prices), 1000):
        print('[OZ] Send prices:', api.send_prices(body_prices[i:i + 1000]))
    for i in range(0, len(body_stocks), 100):
        print('[OZ] Send stocks:', api.send_stocks(body_stocks[i:i + 100]))


if __name__ == '__main__':
    api = OzonAPI(client_id=Config.OZON_CLIENT_ID, api_key=Config.OZON_API_KEY)
    updating_ozon(api, Config.OZON_WAREHOUSE_ID)