import os
import requests


# =========================
# 設定地點
# =========================
LATITUDE = 25.0330
LONGITUDE = 121.5654

# 降雨機率門檻
THRESHOLD = 60


# =========================
# 從 Open-Meteo 取得天氣
# =========================
def get_rain_probability():
    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "daily": "precipitation_probability_max",
        "timezone": "Asia/Taipei",
        "forecast_days": 1
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()

    probability = data["daily"]["precipitation_probability_max"][0]

    return probability


# =========================
# 傳送 Telegram 訊息
# =========================
def send_telegram_message(message):

    # 從環境變數取得，不直接寫在程式裡
    bot_token = os.environ["TELEGRAM_BOT_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    data = {
        "chat_id": chat_id,
        "text": message
    }

    response = requests.post(url, data=data)
    response.raise_for_status()


# =========================
# 主程式
# =========================
def main():

    rain_probability = get_rain_probability()

    print(f"今天降雨機率：{rain_probability}%")

    if rain_probability > THRESHOLD:

        message = (
            f"🌧️ 今日降雨機率為 {rain_probability}%！\n"
            "記得帶傘喔！☂️"
        )

        send_telegram_message(message)

        print("已發送 Telegram 通知！")

    else:

        print("降雨機率未超過門檻，不發送通知。")


if __name__ == "__main__":
    main()
