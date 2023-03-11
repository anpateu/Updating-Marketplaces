import sqlite3
import json


def clear_extra_table():
    conn = sqlite3.connect('products.db')
    c = conn.cursor()
    c.execute("UPDATE extras SET price = 0")
    conn.commit()
    conn.close()


def save_extra_info(api):
    clear_extra_table()
    conn = sqlite3.connect('products.db')
    c = conn.cursor()
    data = api.get_extra_info()
    try:
        for row in data['rows']:
            product = api.get_entity(row['meta']['href'])
            for attrs in product['attributes']:
                if attrs['name'] == 'Доп. наценка (скидка)':
                    code = str(row['code'])
                    price = int(attrs['value'])
                    c.execute('INSERT OR REPLACE INTO extras (code, price) VALUES (?, ?)', (code, price))
                    print(f"[MS] Uploaded extra price - code: {code} price: {price}")
    except json.decoder.JSONDecodeError as e:
        print(f"JSONDecodeError occurred: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
    else:
        conn.commit()
    finally:
        conn.close()