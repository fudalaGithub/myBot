from binance.client import Client
import pandas as pd
import time

api_key = "89ed1c47a4a2ebe2d149fd5b79139d0afbb784d8170eda0792704d2e9cfac29d"
secret_key = "1511914f14f888647c24c818610725d7193b95d14cd06ca3a95ad302539bca0d"
coin = "LTCUSDT"
leverage = 10
size = 100

client = Client(api_key = api_key, api_secret = secret_key, tld = "com", testnet= True)

position_info = client.futures_position_information(symbol=coin)

def buy_long():

    # kaldıraç ayarla
    client.futures_change_leverage(symbol=coin, leverage=leverage)

    client.futures_create_order(symbol=coin, side="BUY", type="MARKET", quantity=size)


def close_long():
    position_info = client.futures_position_information(symbol=coin)
    # pozisyon miktarını belirle
    quantity = abs(float(position_info[0]['positionAmt']))

    # pozisyonu kapat
    client.futures_create_order(symbol=coin, side="SELL", type="MARKET", quantity=quantity, reduceOnly=True)


def buy_short():
    # kaldıraç ayarla
    client.futures_change_leverage(symbol=coin, leverage=leverage)

    client.futures_create_order(symbol=coin, side="SELL", type="MARKET", quantity=size)

def close_short():
    position_info = client.futures_position_information(symbol=coin)
    # pozisyon miktarını belirle
    quantity = abs(float(position_info[0]['positionAmt']))

    # pozisyonu kapat
    client.futures_create_order(symbol=coin, side="BUY", type="MARKET", quantity=quantity, reduceOnly=True)


buy_short()
print("Alindi")
time.sleep(5.5)


close_short()

print("Alindi sAtildi")





#chek_order_status = client.futures_get_order(symbol = coin, orderId = order_open["orderId"])

#futures_position_info = client.futures_position_information(symbol = coin)

# order_close = client.futures_create_order(symbol = "BTCUSDT", side = "SELL",
# client.futures_get_order(symbol = "BTCUSDT", orderId = order_close["orderId"]) # check order status
# client.futures_position_information(symbol = "BTCUSDT")











#while True:
    #client.futures_account()
    #pd.DataFrame(client.futures_account()["assets"])
    #client.futures_account_balance()
    #position = client.futures_position_information(symbol="LTCUSDT")

    #print("Market Price : " + str(position))



