def update_wb(api, warehouse_id, data):
    nums, codes, barcodes = api.get_cards_data()
    with open('data/big.txt', 'r') as file:
        big = [code.strip() for code in file.readlines()]

    body_stocks = [
        {"sku": str(barcode), "amount": int(data['stocks'].get(code, 0))}
        for code, barcode in zip(codes, barcodes)
        if str(barcode) not in big and str(barcode) != '2037297548791'
        ]

    body_prices = [
        {"nmId": int(nmID), "price": int(float(data['prices'].get(code, 0)) * 1.08)}
        for nmID, code in zip(nums, codes)
        if int(float(data['prices'].get(code, 0)) * 1.08) > 0
        ]

    for prices_chunk in [body_prices[i:i + 1000] for i in range(0, len(body_prices), 1000)]:
        print('[WB] Send prices:', api.send_prices(prices_chunk))

    for stocks_chunk in [body_stocks[i:i + 1000] for i in range(0, len(body_stocks), 1000)]:
        print('[WB] Send stocks:', api.send_stocks(stocks_chunk, warehouse_id))