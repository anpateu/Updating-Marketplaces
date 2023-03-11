import pandas as pd
from config import Config


class Sheet:
    def __init__(self):
        self.document_id = Config.GOOGLE_DOCUMENT_ID

    def check_table(self, shop):
        ggl = pd.read_csv(f'https://docs.google.com/spreadsheets/d/{self.document_id}/export?format=csv&gid=0')
        for element in range(ggl.shape[0]):
            table_shop = str(ggl.iloc[element]['Магазин'])
            if shop == table_shop:
                k1 = float(ggl.iloc[element]['Больше_5000'].replace(',', '.'))
                k2 = float(ggl.iloc[element]['Меньше_5000'].replace(',', '.'))
                add = int(ggl.iloc[element]['Наценка'])

        return k1, k2, add