import sqlite3
import pandas as pd
import numpy as np
import math
from google import Sheet


def update_products_table(records):
    conn = sqlite3.connect('products.db')
    c = conn.cursor()
    for record in records:
        stock, price, code = record
        c.execute(
            f'INSERT INTO prices (code, ae) VALUES (?, ?) ON CONFLICT (code) DO UPDATE SET ae = ?',
            (code, price, price))
        c.execute(
            f'INSERT INTO stocks (code, ae) VALUES (?, ?) ON CONFLICT (code) DO UPDATE SET ae = ?',
            (code, stock, stock))
        print(f"[AE] Updated product with code {code}: stock = {stock}, price = {price}")
    conn.commit()
    conn.close()


def load_codes():
    codes_dict = {}
    with sqlite3.connect('products.db') as conn:
        c = conn.cursor()
        for row in c.execute("SELECT * FROM codes"):
            codes_dict[row[1]] = row[0]
    return codes_dict


def load_table_data():
    k1, k2, add = Sheet().check_table('ИП')
    return k1, k2, add


def clear_stocks_table():
    conn = sqlite3.connect('products.db')
    c = conn.cursor()
    c.execute("UPDATE stocks SET ae = 0")
    conn.commit()
    conn.close()


def load_AE():
    print("[AE] Loading data from Excel file...")
    ae_data = pd.read_excel('mail/НОВЫЙ ПОВОРОТ.xls', skiprows=[0,1,2,3,4,5,6])
    ae_data = ae_data.replace(np.nan, 0)
    clear_stocks_table()

    print("[AE] Loading data from Google file...")
    k1, k2, add = load_table_data()
    codes_dict = load_codes()

    records = []
    for i in range(ae_data.shape[0]):
        ae_code = str(ae_data.iloc[i]['Артикул '])
        code = codes_dict.get(ae_code, '')
        if code != '':
            stocks = int(str(ae_data.iloc[i]['Всего']).replace(' ', ''))
            raw = float(str(ae_data.iloc[i]['Ваша ЦЕНА']).replace(' ', '').replace(',', '.'))

            if stocks > 5:
                records.append((stocks, math.ceil(add + (raw * k1)) if raw > 5000 else math.ceil(add + (raw * k2)), code))
            else:
                records.append((0, 0, code))

    print("[AE] Updating products table...")
    update_products_table(records)


if __name__ == '__main__':
    load_AE()