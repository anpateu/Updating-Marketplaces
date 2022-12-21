import os
import shutil
import math
import shelve
from google import Sheet


def remove(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

def load_data_from_MS(api, store_id):
    path_to_data = '..\\..\\data'
    remove(path_to_data)
    data = api.get_stocks(store_id, 1, 0)
    size = int(data['meta']['size'])
    k1, k2, add = Sheet().check_table('ИП')

    for k in range(size//1000 + 1):
        data = api.get_stocks(store_id, 1000, k*1000)
        for i in range(len(data['rows'])):
            market = 0
            code = str(data['rows'][i]['code'])
            with shelve.open(f'{path_to_data}\\extra') as shlv:
                extra = shlv.get(code, 0)
            quantity = max(0, int(round((data['rows'][i]['quantity']), 2)))
            row_price = int(round((data['rows'][i]['price'])/100, 2))

            if row_price != 0:
                k = k1 if row_price > 5000 else k2
                market = math.ceil(add + (row_price * k) + extra)

            with shelve.open(f'{path_to_data}\\stocks') as shlv:
                shlv[code] = quantity
            with shelve.open(f'{path_to_data}\\prices') as shlv:
                shlv[code] = market