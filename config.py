import os

from dotenv import load_dotenv

load_dotenv('..\\..\\.env')


class Config:
    OZON_CLIENT_ID = os.getenv('OZON_CLIENT_ID')
    OZON_API_KEY = os.getenv('OZON_API_KEY')
    OZON_WAREHOUSE_ID = os.getenv('OZON_WAREHOUSE_ID')
    WB_API_KEY = os.getenv('WB_API_KEY')
    WB_NEW_API_KEY = os.getenv('WB_NEW_API_KEY')
    WB_WAREHOUSE_ID = os.getenv('WB_WAREHOUSE_ID')
    MS_API_KEY = os.getenv('MS_API_KEY')
    MS_STORE_ID = os.getenv('MS_STORE_ID')
    GOOGLE_DOCUMENT_ID = os.getenv('GOOGLE_DOCUMENT_ID')