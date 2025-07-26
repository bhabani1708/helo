import requests
import time
import os


COINGLASS_API_KEY = os.getenv("5c1ec8ed34f842ea89eb770c44a43a2f")


TELEGRAM_BOT_TOKEN = os.getenv("7181559765:AAGAr04ECDvpveY5CaW-n2iHmV4xO1JxPRs")
TELEGRAM_CHAT_ID = os.getenv("1727521702")

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    requests.post(url, data=data)

def fetch_data():
    url = "https://open-api.coinglass.com/public/v2/futures/longShortChart"
    headers = {
        "coinglassSecret": COINGLASS_API_KEY
    }
    params = {
        "symbol": "BTC",
        "interval": "15m",
    }
    res = requests.get(url, headers=headers, params=params)
    return res.json()

def analyze_and_send():
    try:
        data = fetch_data()
        latest = data["data"][-1]
        long_ratio = latest["longAccount"]
        short_ratio = latest["shortAccount"]

        direction = "🔼 LONG" if long_ratio > short_ratio else "🔽 SHORT"
        msg = f"*BTC Signal (15m)*\nDirection: {direction}\nLongs: {long_ratio:.2f}%\nShorts: {short_ratio:.2f}%"

        send_telegram(msg)
    except Exception as e:
        send_telegram(f"❌ Error: {str(e)}")

while True:
    analyze_and_send()
    time.sleep(900)  # 15 min
