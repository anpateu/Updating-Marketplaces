import sqlite3
from math import ceil
from google import Sheet
from config import Config
from API.ms import MoySkladAPI


def get_extra_data(code):
    conn = sqlite3.connect('products.db')
    c = conn.cursor()
    c.execute('SELECT price FROM extras WHERE code = ?', (code,))
    extra_data = c.fetchone()
    conn.close()
    return extra_data[0] if extra_data and isinstance(extra_data[0], (int, float)) else 0


def load_data_from_MS(api, store_id, warehouse):
    conn = sqlite3.connect('products.db')
    c = conn.cursor()
    c.execute(f'UPDATE stocks SET {warehouse} = 0')
    conn.commit()
    conn.close()
    print(f"[DB] Warehouse {warehouse} stock set to 0")

    data = api.get_stocks(store_id, 1, 0)
    size = int(data['meta']['size'])
    k1, k2, add = Sheet().check_table('ИП')
    print(f"[MS] Loaded google: {k1} - {k2} - {add} // size: {size}")

    def process_row(row):
        code = str(row['code'])
        quantity = max(0, int(round((row['quantity']), 2)))
        row_price = ceil(round((row['price']) / 100, 2))

        market = 0
        if row_price != 0:
            k = k1 if row_price > 5000 else k2
            market = ceil(add + (row_price * k) + get_extra_data(code))
        print(f"[MS] Process row - code: {code} quantity: {quantity} market: {market}")
        return code, quantity, market

    conn = sqlite3.connect('products.db')
    c = conn.cursor()

    for k in range(size // 1000 + 1):
        data = api.get_stocks(store_id, 1000, k * 1000)
        rows_data = data['rows']
        rows = [process_row(row) for row in rows_data]
        for code, quantity, market in rows:
            c.execute(
                f'INSERT INTO prices (code, {warehouse}) VALUES (?, ?) ON CONFLICT (code) DO UPDATE SET {warehouse} = ?',
                (code, market, market))
            c.execute(
                f'INSERT INTO stocks (code, {warehouse}) VALUES (?, ?) ON CONFLICT (code) DO UPDATE SET {warehouse} = ?',
                (code, quantity, quantity))

        print(f"[DB] Warehouse {warehouse} rows processed: {len(rows)}")

    conn.commit()
    conn.close()
    print(f"[DB] Warehouse {warehouse} done")


if __name__ == '__main__':
    load_data_from_MS(MoySkladAPI(api_key=Config.MS_API_KEY), Config.MS_STORE_1_ID, 'ip')
    load_data_from_MS(MoySkladAPI(api_key=Config.MS_API_KEY), Config.MS_STORE_2_ID, 'np')