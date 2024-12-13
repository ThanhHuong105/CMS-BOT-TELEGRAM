from flask import Flask, request, jsonify
import requests
import logging

# Cấu hình API Token của Telegram và URL Apps Script
TELEGRAM_API_TOKEN = "7925656043:AAEbWFSv7_9WlWi78Hxw6Z5jigY2KgvAeg4"  # Thay bằng API Token Telegram của bạn
APPS_SCRIPT_URL = "https://script.googleusercontent.com/macros/echo?user_content_key=eZg5cqestD_-p8229ybc64qxrDso1LdXk2xrq0KH4uzcF6Jvtf2pON9iu2-JfM_k1cnsof4rLtlzUxtOFzKIppUk6fyT2hjDm5_BxDlH2jW0nuo2oDemN9CCS2h10ox_1xSncGQajx_ryfhECjZEnOg--23PBBdckXFcygtPsOKqHmK0oLQONMmr8wntXkebPTDQLkJ7oAxGa7q2NBhra6pn7W-NCXYKkEYoGidVjL574qmCBla3Ndz9Jw9Md8uu&lib=M4vLeyyNWWmip8P5l2GSUYWBrNDogpDCq"  # URL Apps Script của bạn

# Tạo ứng dụng Flask
app = Flask(__name__)

# Thiết lập logging chi tiết để kiểm tra log
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


@app.route("/", methods=["POST"])
def webhook():
    """
    Hàm xử lý webhook từ Telegram.
    """
    try:
        # Nhận dữ liệu từ Telegram
        data = request.json
        logging.info(f"Dữ liệu nhận được từ Telegram: {data}")

        # Kiểm tra tính hợp lệ của dữ liệu
        if not data or "message" not in data:
            logging.error("Dữ liệu không hợp lệ hoặc thiếu trường 'message'.")
            return jsonify({"status": "error", "message": "Invalid data"}), 400

        # Gửi dữ liệu tới Apps Script
        response = requests.post(APPS_SCRIPT_URL, json=data)
        logging.info(f"Phản hồi từ Apps Script: {response.text}")

        # Phản hồi lại cho Telegram
        return jsonify({"status": "success", "message": "Dữ liệu đã được xử lý"}), 200
    except Exception as e:
        logging.error(f"Lỗi trong webhook: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500


def set_webhook():
    """
    Thiết lập webhook Telegram bot trỏ tới Railway URL.
    """
    try:
        # URL Railway (thay thế bằng URL của bạn trên Railway)
        railway_url = "https://<your-railway-app-url>.up.railway.app/"  # Thay bằng URL Railway của bạn
        telegram_url = f"https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/setWebhook"

        # Thiết lập webhook Telegram
        response = requests.post(telegram_url, data={"url": railway_url})
        logging.info(f"Kết quả thiết lập webhook: {response.json()}")
    except Exception as e:
        logging.error(f"Lỗi khi thiết lập webhook: {str(e)}")


if __name__ == "__main__":
    set_webhook()  # Thiết lập webhook khi chạy bot lần đầu
    app.run(host="0.0.0.0", port=5000)  # Chạy ứng dụng Flask trên cổng 5000

