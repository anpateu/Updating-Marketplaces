import pandas as pd


COLUMN_NAMES = {
    '972200353': {'n1': 'Себестоимость', 'n2': 'Цена_продажи'},
    '1970113351': {'n1': 'Дни_хранения', 'n2': 'Цена_продажи'},
    '1221897230': {'n1': 'Дни_хранения', 'n2': 'Опт'}
}


def check_markup(doc, gid):
    n1 = COLUMN_NAMES[gid]['n1']
    n2 = COLUMN_NAMES[gid]['n2']
    url = f'https://docs.google.com/spreadsheets/d/{doc}/export?format=csv&gid={gid}'
    matrix_price = pd.read_csv(url)
    coefficients = {}
    for index, row in matrix_price.iterrows():
        coefficients[int(row[n1])] = float(row[n2].replace(',', '.'))
    return coefficients


def check_markets(doc, shop='ИП'):
    url = f'https://docs.google.com/spreadsheets/d/{doc}/export?format=csv&gid=0'
    ggl = pd.read_csv(url)
    coefficients = []
    for element in range(ggl.shape[0]):
        table_shop = str(ggl.iloc[element]['Магазин'])
        if shop == table_shop:
            coefficients.append(float(ggl.iloc[element]['Больше_5000'].replace(',', '.')))
            coefficients.append(float(ggl.iloc[element]['Меньше_5000'].replace(',', '.')))
            add = int(ggl.iloc[element]['Наценка'])

    return coefficients, add