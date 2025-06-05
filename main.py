import tweepy
import requests
import re
import time
import schedule

# === TWITTER API KEYS ===
API_KEY = "ok8wtAYWITnOcf4z8cgAXrjXd"
API_SECRET = "07W9sPBmNfdQVqU4CNjuuUtt9UU22aQKktPaL1qf2hAa7tmhWb"
ACCESS_TOKEN = "1930762725883260928-02CLkvUHlmpoWykCpicD6NxOjq3tyW"
ACCESS_SECRET = "52Or9dOJaiVwkHqzTWI9AuRPYhNPRyw0mF9au72L1RgbV"

# === TELEGRAM BOT INFO ===
TELEGRAM_BOT_TOKEN = "7612105153:AAGhnBG4VdKtoocln0BxIH5etKfqcuirZI"
TELEGRAM_CHAT_USERNAME = "CrazyLazyD"

auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": f"@{TELEGRAM_CHAT_USERNAME}",
        "text": message,
        "parse_mode": "Markdown"
    }
    requests.post(url, data=payload)

def parse_and_alert(tweet):
    text = tweet.text
    match = re.search(r"(\d+[\.,]?\d*[MK]?)\s+([A-Z]+)\s+transferred.*from\s+.*to\s+.*", text)
    if not match:
        return

    amount_raw, symbol = match.groups()
    amount = float(amount_raw.replace(",", "").replace("M", "").replace("K", ""))
    if "M" in amount_raw:
        amount *= 1_000_000
    elif "K" in amount_raw:
        amount *= 1_000

    if amount > 1_000_000:
        message = f"🐋 *Whale Alert*\n• {amount:,.0f} {symbol} verplaatst\n• [Bekijk tweet](https://twitter.com/whale_alert/status/{tweet.id})"
        send_to_telegram(message)

def fetch_whale_tweets():
    tweets = api.user_timeline(screen_name="whale_alert", count=10, tweet_mode="extended")
    for tweet in tweets:
        parse_and_alert(tweet)

schedule.every(10).minutes.do(fetch_whale_tweets)

print("✅ Whale Alert bot draait...")
while True:
    schedule.run_pending()
    time.sleep(1)
