from flask import Flask, request
import requests

app = Flask(__name__)

TELEGRAM_API_TOKEN = "7925656043:AAEbWFSv7_9WlWi78Hxw6Z5jigY2KgvAeg4"
WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbxyz/exec"  # URL từ Apps Script

@app.route("/", methods=["POST"])
def webhook():
    # Nhận dữ liệu từ Telegram
    data = request.json
    print("Nhận dữ liệu từ Telegram:", data)

    # Chuyển dữ liệu đến Google Apps Script
    response = requests.post(WEBHOOK_URL, json=data)
    print("Phản hồi từ Apps Script:", response.json())

    return {"status": "success", "message": "Đã chuyển dữ liệu tới Apps Script."}

def set_webhook():
    url = f"https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/setWebhook"
    webhook_url = "https://your-railway-url.up.railway.app/"  # Railway URL của bạn
    response = requests.post(url, data={"url": webhook_url})
    print(response.json())

if __name__ == "__main__":
    set_webhook()
    app.run(host="0.0.0.0", port=5000)
