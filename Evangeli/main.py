from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ValidationError
from dotenv import load_dotenv
import logging
import requests
import os

from binance.client import Client
from binance.exceptions import BinanceAPIException
from binance.enums import *

load_dotenv()  # take environment variables from .env.
LINE_NOTIFY_TOKEN = os.getenv("LINE_NOTIFY_TOKEN")
LINE_NOTIFY_URL = os.getenv("LINE_NOTIFY_URL")

# Initialize the Binance Client
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")
TESTNET = os.getenv("BINANCE_TESTNET", "True").lower() in ["true", "1"]

FIX_USDT_AMOUNT = float(os.getenv("FIX_USDT_AMOUNT", "250"))  # Default is 250
LEVERAGE = int(os.getenv("LEVERAGE", "1"))  # Default leverage is 1


client = Client(API_KEY, API_SECRET, testnet=TESTNET)
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

try:
    client.ping()
    time_res = client.get_server_time()
    account_info = client.get_account_status()
    exangeInfo = client.get_exchange_info()
    symbolInfo = client.get_symbol_info('BNBBTC')
    tickerInfo = client.get_all_tickers()
    info = client.get_account_snapshot(type='FUTURES')
except BinanceAPIException as e:
    logging.error(f"Error: {e}")
    raise HTTPException(status_code=400, detail=f"Error: {e}")

# 定義 BaseModel 結構，webhook 結構必須要對映，否則會報錯
class Bar(BaseModel):
    time: str
    open: str
    high: str
    low: str
    close: str
    volume: str

class Strategy(BaseModel):
    position_size: str
    order_action: str
    order_contracts: str
    order_price: str
    order_id: str
    market_position: str
    market_position_size: str
    prev_market_position: str
    prev_market_position_size: str

class TradingViewWebhook(BaseModel):
    phassphrase: str
    time: str
    exchange: str
    ticker: str
    bar: Optional[Bar] = None
    strategy: Optional[Strategy] = None

tradingViewHookApp = FastAPI()

@tradingViewHookApp.post("/webhook")
async def receive_webhook(webhook_data: TradingViewWebhook):
    try:
        json_text = webhook_data.model_dump_json(indent=2)
        item_dict = webhook_data.model_dump()
        # print(json_text)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=f"Invalid data: {e.errors()}")

    # 設定傳送到 LINE Notify 的訊息格式
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Bearer {LINE_NOTIFY_TOKEN}'
    }
    data = {'message': f'\n{json_text}'}

    # 傳送訊息到 LINE Notify
    response = requests.post(LINE_NOTIFY_URL, headers=headers, data=data)

    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Message not sent. LINE Notify API error.")
    
    return {"message": "Message sent to LINE Notify successfully!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app="main:tradingViewHookApp", host="0.0.0.0", port=80, reload=True)