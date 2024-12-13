from flask import Flask, request
import requests

app = Flask(__name__)

# Thay bằng API Token của bạn
TELEGRAM_API_TOKEN = "7925656043:AAEbWFSv7_9WlWi78Hxw6Z5jigY2KgvAeg4"
# URL Web App Google Apps Script của bạn
WEBHOOK_URL = "https://script.googleusercontent.com/macros/s/XXXXXX/exec"  # Thay XXXXXX bằng URL Web App của bạn

@app.route("/", methods=["POST"])
def webhook():
    try:
        # Nhận dữ liệu từ Telegram
        data = request.json
        print("Dữ liệu nhận được từ Telegram:", data)

        # Gửi dữ liệu tới Google Apps Script
        response = requests.post(WEBHOOK_URL, json=data)
        print("Phản hồi từ Google Apps Script:", response.json())

        return {"status": "success", "message": "Dữ liệu đã được xử lý"}, 200
    except Exception as e:
        print("Lỗi trong webhook:", e)
        return {"status": "error", "message": str(e)}, 500


def set_webhook():
    # Thiết lập webhook cho Telegram bot
    url = f"https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/setWebhook"
    webhook_url = "https://your-railway-app-url.up.railway.app/"  # Thay bằng URL Railway của bạn
    response = requests.post(url, data={"url": webhook_url})
    print("Kết quả thiết lập webhook:", response.json())


if __name__ == "__main__":
    set_webhook()  # Thiết lập webhook khi chạy bot lần đầu
    app.run(host="0.0.0.0", port=5000)
