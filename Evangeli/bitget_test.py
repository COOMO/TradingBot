from bitget.v1.mix import order_api as maxOrderApi
from bitget import bitget_api as baseApi
from bitget.exceptions import BitgetAPIException
from dotenv import load_dotenv

import os

load_dotenv()  # take environment variables from .env.

API_KEY = os.getenv("BITGET_API_KEY")
API_SECRET = os.getenv("BITGET_API_SECRET")
API_PASSPHRASE = os.getenv("BITGET_API_PASSPHRASE")

if __name__ == '__main__':
    apiKey = API_KEY
    secretKey = API_SECRET
    passphrase = API_PASSPHRASE

    # Demo 1:place order
    maxOrderApi = maxOrderApi.OrderApi(apiKey, secretKey, passphrase)
    try:
        params = {}
        params["symbol"] = "BTCUSDT_UMCBL"
        params["marginCoin"] = "USDT"
        params["side"] = "open_long"
        params["orderType"] = "limit"
        params["price"] = "27012"
        params["size"] = "0.01"
        params["timInForceValue"] = "normal"
        response = maxOrderApi.placeOrder(params)
        print(response)
    except BitgetAPIException as e:
        print("error:" + e.message)

    # Demo 2:place order by post directly
    baseApi = baseApi.BitgetApi(apiKey, secretKey, passphrase)
    try:
        params = {}
        params["symbol"] = "BTCUSDT_UMCBL"
        params["marginCoin"] = "USDT"
        params["side"] = "open_long"
        params["orderType"] = "limit"
        params["price"] = "27012"
        params["size"] = "0.01"
        params["timInForceValue"] = "normal"
        response = baseApi.post("/api/mix/v1/order/placeOrder", params)
        print(response)
    except BitgetAPIException as e:
        print("error:" + e.message)

    # Demo 3:send get request
    try:
        params = {}
        params["productType"] = "umcbl"
        response = baseApi.get("/api/mix/v1/market/contracts", params)
        print(response)
    except BitgetAPIException as e:
        print("error:" + e.message)

    # Demo 4:send get request with no params
    try:
        response = baseApi.get("/api/spot/v1/account/getInfo", {})
        print(response)
    except BitgetAPIException as e:
        print("error:" + e.message)

    # Demo 5:send get request
    try:
        params = {}
        params["symbol"] = "AIUSDT"
        params["businessType"] = "spot"
        response = baseApi.get("/api/v2/common/trade-rate", params)
        print(response)
    except BitgetAPIException as e:
        print("error:" + e.message)