import os
import time
import sqlite3
import schedule
import concurrent.futures
import pandas as pd
from config import Config
from API.ms import MoySkladAPI
from API.ozon import OzonAPI
from API.wb import WildberriesAPI
from load_data import load_data_from_MS
from updating_ozon import update_ozon
from updating_wb import update_wb
from extra import save_extra_info
from mail import export_mail
from autoelectrica import load_AE


def create_db():
    conn = sqlite3.connect('products.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE prices
                 (code TEXT PRIMARY KEY,
                  ae INTEGER,
                  ip INTEGER,
                  np INTEGER,
                  bs INTEGER);''')
    c.execute('''CREATE TABLE stocks
                 (code TEXT PRIMARY KEY,
                  ae INTEGER,
                  ip INTEGER,
                  np INTEGER,
                  bs INTEGER);''')
    c.execute('''CREATE TABLE codes
                 (code TEXT PRIMARY KEY,
                  ae TEXT);''')
    c.execute('''CREATE TABLE extras
                 (code TEXT PRIMARY KEY,
                  price INTEGER);''')
    c.execute('''CREATE TABLE moysklad
                 (code TEXT PRIMARY KEY,
                  sale_price INTEGER,
                  opt INTEGER,
                  marketplaces INTEGER);''')
    conn.commit()
    conn.close()
    print("[DB] Created database")


def update_codes_table():
    df = pd.read_excel('matching.xlsx')
    conn = sqlite3.connect('products.db')
    c = conn.cursor()
    for index, row in df.iterrows():
        code = str(row['QID'])
        ae = str(row['Код (поставщик)'])
        c.execute("INSERT OR REPLACE INTO codes (code, ae) VALUES (?, ?)", (code, ae))
    conn.commit()
    conn.close()
    print("[DB] Updated AE codes")


def get_product_data(*warehouses):
    conn = sqlite3.connect('products.db')
    c = conn.cursor()

    stocks = {}
    prices = {}
    for warehouse in warehouses:
        c.execute(f"SELECT code, COALESCE({warehouse}, 0) FROM stocks")
        rows = c.fetchall()
        for code, quantity in rows:
            stocks.setdefault(code, 0)
            stocks[code] += quantity

        c.execute(f"SELECT code, COALESCE({warehouse}, 0) FROM prices")
        rows = c.fetchall()
        for code, price in rows:
            prices.setdefault(code, 0)
            if price > prices[code]:
                prices[code] = price

    conn.close()
    return {'stocks': stocks, 'prices': prices}


def start_updating(api_ozon, api_wb):
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        future1 = executor.submit(update_ozon, api_ozon, Config.OZON_WAREHOUSE_1_ID, get_product_data('ip'))
        future2 = executor.submit(update_ozon, api_ozon, Config.OZON_WAREHOUSE_2_ID, get_product_data('np', 'ae'))
        future3 = executor.submit(update_wb, api_wb, Config.WB_WAREHOUSE_ID, get_product_data('ip', 'np', 'ae'))
        concurrent.futures.wait([future1, future2, future3])


def hourly_tasks(api_ms, api_ozon, api_wb):
    save_extra_info(api_ms)
    load_data_from_MS(api_ms, Config.MS_STORE_1_ID, 'ip')
    load_data_from_MS(api_ms, Config.MS_STORE_2_ID, 'np')
    start_updating(api_ozon, api_wb)


def daily_tasks():
    export_mail(Config.GMAIL_USERNAME, Config.GMAIL_PASSWORD)
    load_AE()


def schedule_tasks():
    api_ozon = OzonAPI(client_id=Config.OZON_CLIENT_ID, api_key=Config.OZON_API_KEY)
    api_wb = WildberriesAPI(api_key=Config.WB_API_KEY)
    api_ms = MoySkladAPI(api_key=Config.MS_API_KEY)

    schedule.every().day.at("07:30").do(daily_tasks)
    schedule.every().hour.at(":55").do(hourly_tasks, api_ms, api_ozon, api_wb)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    if not os.path.exists('products.db'):
        create_db()
        update_codes_table()
    schedule_tasks()