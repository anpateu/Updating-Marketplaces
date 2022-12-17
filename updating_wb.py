import shelve
import math
from config import Config
from API.wb import WildberriesAPI


def open_shelve(path, code):
    try:
        with shelve.open(path) as data:
            info = data[code]
    except:
        info = 0
    return info

def load_products(total):
    total = math.ceil(total / 1000)
    wb_codes, barcodes, nums = [], [], []
    for k in range(total):
        data = api.get_products(k * 1000, 1000)[0]
        for element in data['stocks']:
            wb_codes.append(element['article'])
            barcodes.append(element['barcode'])
            nums.append(element['nmId'])
    return wb_codes, barcodes, nums

def updating_wb(api, warehouseId):
    total = api.get_products(0, 1)[1]
    codes, barcodes, nums = load_products(total)
    body_stocks, body_prices = [], []

    for i in range(len(codes)):
        nmID = nums[i]
        code = codes[i]
        barcode = barcodes[i]
        stocks = open_shelve('data/stocks', code)
        price = open_shelve('data/prices', code)
        price = int(float(price)*1.08)

        product_stocks = {
            "sku": str(barcode),
            "amount": int(stocks)
            }
        body_stocks.append(product_stocks)

        if price > 0:
            product_prices = {
                "nmId": int(nmID),
                "price": int(price)
                }
            body_prices.append(product_prices)

    for i in range(0, len(body_prices), 1000):
        print('[WB] Send prices:', api.send_prices(body_prices[i:i + 1000]))
    for i in range(0, len(body_stocks), 1000):
        print('[WB] Send stocks:', api.send_stocks(body_stocks[i:i + 1000], warehouseId))

if __name__ == '__main__':
    api = WildberriesAPI(api_key=Config.WB_NEW_API_KEY)
    updating_wb(api, Config.WB_WAREHOUSE_ID)