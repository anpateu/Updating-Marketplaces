import os

from dotenv import load_dotenv

load_dotenv('..\\..\\.env')


class Config:
    OZON_CLIENT_ID = os.getenv('OZON_CLIENT_ID')
    OZON_API_KEY = os.getenv('OZON_API_KEY')
    OZON_WAREHOUSE_1_ID = os.getenv('OZON_WAREHOUSE_1_ID')
    OZON_WAREHOUSE_2_ID = os.getenv('OZON_WAREHOUSE_2_ID')
    WB_API_KEY = os.getenv('WB_API_KEY')
    WB_WAREHOUSE_ID = os.getenv('WB_WAREHOUSE_ID')
    MS_API_KEY = os.getenv('MS_API_KEY')
    MS_STORE_1_ID = os.getenv('MS_STORE_1_ID')
    MS_STORE_2_ID = os.getenv('MS_STORE_2_ID')
    GOOGLE_DOCUMENT_ID = os.getenv('GOOGLE_DOCUMENT_ID')
    GOOGLE_PRICE_SHEET = os.getenv('GOOGLE_PRICE_SHEET')
    GOOGLE_SALE_SHEET = os.getenv('GOOGLE_SALE_SHEET')
    GOOGLE_OPT_SHEET = os.getenv('GOOGLE_OPT_SHEET')
    GMAIL_USERNAME = os.getenv('GMAIL_USERNAME')
    GMAIL_PASSWORD = os.getenv('GMAIL_PASSWORD')