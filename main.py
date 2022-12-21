import pytz
import time
import datetime
import traceback
from config import Config
from API.ms import MoySkladAPI
from API.ozon import OzonAPI
from API.wb import WildberriesAPI
from load_data import load_data_from_MS
from updating_ozon import update_ozon
from updating_wb import update_wb


def start_updating(api_ms, api_ozon, api_wb):
    load_data_from_MS(api_ms, Config.MS_STORE_ID)
    update_ozon(api_ozon, Config.OZON_WAREHOUSE_ID)
    update_wb(api_wb, Config.WB_WAREHOUSE_ID)


if __name__ == '__main__':
    api_ozon = OzonAPI(client_id=Config.OZON_CLIENT_ID, api_key=Config.OZON_API_KEY)
    api_wb = WildberriesAPI(api_key=Config.WB_NEW_API_KEY)
    api_ms = MoySkladAPI(api_key=Config.MS_API_KEY)
    while True:
        current_date = datetime.datetime.now(pytz.timezone('Europe/Moscow'))
        print(f'\n{current_date.strftime("[%H:%M:%S]")} Starting...')
        try:
            start_updating(api_ms, api_ozon, api_wb)
        except Exception as e:
            print(traceback.format_exc())
        time.sleep(600)