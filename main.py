import math
from flask import Flask, request
from binance.client import Client
import pandas as pd
import time

api_key = "89ed1c47a4a2ebe2d149fd5b79139d0afbb784d8170eda0792704d2e9cfac29d"
secret_key = "1511914f14f888647c24c818610725d7193b95d14cd06ca3a95ad302539bca0d"

coin = "LTCUSDT"
leverage = 20

client = Client(api_key=api_key, api_secret=secret_key, tld="com", testnet=True)

# Calculate how much ETH $200 can buy
size = 1

print("Connected to Binance")
position_info = client.futures_position_information(symbol=coin)

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/apiBuy123456789', methods=['POST'])
def handle_request_buy():
    data = request.json
    name = data['key']
    if name == "BUY":
        buy_long()

    return name


@app.route('/apiSell123456789', methods=['POST'])
def handle_request_sell():
    data = request.json
    name = data['key1']
    # if name == "SELL":
    # buy_short()
    # time.sleep(1)
    # buy_short()
    # time.sleep(2)
    # buy_short()
    buy_short_limit()

    return name


@app.route('/apiStrategy123456789', methods=['POST'])
def handle_request_strategy():
    data = request.json
    alert = data['alert']
    price = data['price']

    if alert == "1":
        buy_long_limit(float(price))
        roe_calculator("LONG")
    elif alert == "-1":
        buy_short_limit(float(price))
        roe_calculator("SHORT")
    else:
        pass
    text = 'Alert : ' + alert + 'Price : ' + price

    return text


def buy_long_limit(alertPrice):
    client.futures_change_leverage(symbol=coin, leverage=leverage)
    piyasa_fiyati = alertPrice
    position_info = client.futures_position_information(symbol=coin)

    if abs(float(position_info[0]['positionAmt'])) > 0:
        close_short()
        time.sleep(0.2)
        client.futures_create_order(symbol=coin, side='BUY', type='LIMIT', timeInForce='GTC', quantity=size,
                            price=piyasa_fiyati)
    else:
        client.futures_create_order(symbol=coin, side='BUY', type='LIMIT', timeInForce='GTC', quantity=size,
                            price=piyasa_fiyati)


def buy_short_limit(alertPrice):
    client.futures_change_leverage(symbol=coin, leverage=leverage)
    piyasa_fiyati = alertPrice
    position_info = client.futures_position_information(symbol=coin)

    if abs(float(position_info[0]['positionAmt'])) > 0:
        close_long()
        time.sleep(0.2)
        client.futures_create_order(symbol=coin, side='SELL', type='LIMIT', timeInForce='GTX', quantity=size,
                            price=piyasa_fiyati)
    else:
        client.futures_create_order(symbol=coin, side='SELL', type='LIMIT', timeInForce='GTX', quantity=size,
                            price=piyasa_fiyati)



def close_long():
    position_info = client.futures_position_information(symbol=coin)
    # pozisyon miktarını belirle
    quantity = abs(float(position_info[0]['positionAmt']))

    # pozisyonu kapat
    client.futures_create_order(symbol=coin, side="SELL", type="MARKET", quantity=quantity)

def close_short():
    position_info = client.futures_position_information(symbol=coin)
    # pozisyon miktarını belirle
    quantity = abs(float(position_info[0]['positionAmt']))

    # pozisyonu kapat
    client.futures_create_order(symbol=coin, side="BUY", type="MARKET", quantity=quantity)


def roe_calculator(position):
    status = True
    procent = 2
    position = position
    stoplos = 15

    while True:
        try:
            balance = client.futures_account_balance()
            time.sleep(0.25)
            account = client.futures_account()
        except Exception as e:
            print(e.message)
            pass

        usdtbalance = 0

        for b1 in account['assets']:
            if b1['asset'] == 'USDT':
                intialmargin = float(b1['initialMargin'])
                unrealizedprofit = float(b1['unrealizedProfit'])
                pnl = float(b1['crossUnPnl'])
                roe = unrealizedprofit / intialmargin * 100

        print('PNL: ' + str(pnl) + 'USDT')
        print('ROE: ' + str(roe) + '%')
        if roe > procent:
            if position == "LONG":
                close_long()
                break
            elif position == "SHORT":
                close_short()
                break
            else:
                print('PNL: ' + str(pnl) + 'USDT')
                print('ROE: ' + str(roe) + '%')

        if roe > stoplos:
            if position == "LONG":
                close_long()
                break
            elif position == "SHORT":
                close_short()
                break
            else:
                pass



def cancel_open_orders():
    #open_orders = client.futures_get_open_orders(symbol=coin)

    #open_order_ID = open_orders[0]["orderId"]

    #print(open_order_ID)

    client.futures_cancel_all_open_orders(symbol=coin)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=123)
