from markup import check_markup, check_markets
from config import Config
from API.ms import MoySkladAPI
from math import ceil
import sqlite3


def get_extra_data(code):
    conn = sqlite3.connect('products.db')
    c = conn.cursor()
    c.execute('SELECT price FROM extras WHERE code = ?', (code,))
    extra_data = c.fetchone()
    conn.close()
    return extra_data[0] if extra_data and isinstance(extra_data[0], (int, float)) else 0


def get_k(data, coefficients):
    for key in sorted(coefficients.keys(), reverse=True):
        if data > key:
            k = coefficients[key]
            break
    else:
        k = coefficients[0]
    return k


def create_element(entity, sale_price, opt, marketplaces):
    PRICES_IDS = {
        'b250a7e0-373c-11ed-0a80-0f7000243ac5': sale_price * 100.0,
        '8e86c2d2-3827-11ed-0a80-07a0003adcc6': opt * 100.0,
        '8e86c468-3827-11ed-0a80-07a0003adcc7': marketplaces * 100.0
    }

    meta = {
        "href": entity,
        "type": "product",
    }

    sale_prices = []
    for price_id, price in PRICES_IDS.items():
        sale_prices.append({
            "value": price,
            "priceType": {
                "meta": {
                    "href": f"https://online.moysklad.ru/api/remap/1.2/context/companysettings/pricetype/{price_id}",
                    "type": "pricetype",
                }
            }
        })

    element = {
        "meta": meta,
        "salePrices": sale_prices
    }

    return element


def process_row(row):
    code = str(row['code'])
    href = str(row['meta']['href'])
    price = ceil(round((row['price']) / 100, 2))
    days = int(row['stockDays'])
    return code, href, price, days


def start_pricing(api):
    doc = Config.GOOGLE_DOCUMENT_ID
    gid_price = Config.GOOGLE_PRICE_SHEET
    gid_sale = Config.GOOGLE_SALE_SHEET
    gid_opt = Config.GOOGLE_OPT_SHEET

    store1 = Config.MS_STORE_1_ID
    store2 = Config.MS_STORE_2_ID
    stores = [store1, store2]

    market = check_markets(doc)
    k_dict = {
        'gid_price': check_markup(doc, gid_price),
        'gid_sale': check_markup(doc, gid_sale),
        'gid_opt': check_markup(doc, gid_opt)
    }

    data = api.get_all_products(stores, 1, 0)
    size = int(data['meta']['size'])
    prices = []
    body = []

    for k in range(size // 1000 + 1):
        data = api.get_all_products(stores, 1000, k * 1000)
        rows_data = data['rows']
        rows = [process_row(row) for row in rows_data]
        for code, href, price, days in rows:
            extra = get_extra_data(code)
            sale_price_k1 = get_k(price, k_dict['gid_price'])
            sale_price_k2 = get_k(days, k_dict['gid_sale'])
            sale_price = int(price * (sale_price_k1 + sale_price_k2) + 9) // 10 * 10 + extra
            opt = ceil(price * get_k(days, k_dict['gid_opt']))
            market_k = market[0][0] if price > 5000 else market[0][1]
            marketplaces = ceil(market[1] + (price * market_k) + extra)
            prices.append((code, href, sale_price, opt, marketplaces))

    conn = sqlite3.connect('products.db')
    c = conn.cursor()
    for code, entity, sale_price, opt, marketplaces in prices:
        c.execute('SELECT sale_price, opt, marketplaces FROM moysklad WHERE code = ?', (code,))
        row = c.fetchone()

        if row and (row[0] != sale_price or row[1] != opt or row[2] != marketplaces):
            c.execute('UPDATE moysklad SET sale_price = ?, opt = ?, marketplaces = ? WHERE code = ?',
                (sale_price, opt, marketplaces, code))
            print(f"[MS] UPDATE {code} - sale_price: {sale_price} opt: {opt} marketplaces: {marketplaces}")
            conn.commit()
            data_element = create_element(entity, sale_price, opt, marketplaces)
            body.append(data_element)
        elif not row:
            c.execute('INSERT INTO moysklad (code, sale_price, opt, marketplaces) VALUES (?, ?, ?, ?)',
                (code, sale_price, opt, marketplaces))
            print(f"[MS] INSERT {code} - sale_price: {sale_price} opt: {opt} marketplaces: {marketplaces}")
            conn.commit()
            data_element = create_element(entity, sale_price, opt, marketplaces)
            body.append(data_element)

        if len(body) == 100:
            api.update_product(body)
            body = []

    if body:
        api.update_product(body)

    conn.close()


if __name__ == '__main__':
    api_ms = MoySkladAPI(api_key=Config.MS_API_KEY)
    start_pricing(api_ms)