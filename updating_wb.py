import shelve
import math


def load_products(api, total):
    total = math.ceil(total / 1000)
    wb_codes, barcodes, nums = [], [], []
    for k in range(total):
        data = api.get_products(k * 1000, 1000)
        for element in data['stocks']:
            wb_codes.append(element['article'])
            barcodes.append(element['barcode'])
            nums.append(element['nmId'])
    return wb_codes, barcodes, nums

def update_wb(api, warehouse_id):
    path_to_data = '..\\..\\data'
    total = api.get_products(0, 1)['total']
    codes, barcodes, nums = load_products(api, total)
    body_stocks, body_prices = [], []

    for i in range(len(codes)):
        nmID = nums[i]
        code = codes[i]
        barcode = barcodes[i]
        with shelve.open(f'{path_to_data}\\stocks') as data:
            stocks = data.get(code, 0)
        with shelve.open(f'{path_to_data}\\prices') as data:
            price = data.get(code, 0)
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
        print('[WB] Send stocks:', api.send_stocks(body_stocks[i:i + 1000], warehouse_id))