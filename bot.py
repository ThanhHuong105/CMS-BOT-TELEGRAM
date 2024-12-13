from flask import Flask, request
import requests

app = Flask(__name__)

TELEGRAM_API_TOKEN = "7925656043:AAEbWFSv7_9WlWi78Hxw6Z5jigY2KgvAeg4"
WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbylzS50Un2l80D8DW-Nopypl9D0mAMZNoR_TArNXYb9CLk1XVAYQtifPVu-BrPAVXT2Og/exec"

@app.route("/", methods=["GET", "POST"])
def webhook():
    if request.method == "POST":
        data = request.json
        # Forward data to Google Apps Script
        response = requests.post(WEBHOOK_URL, json=data)
        return {"status": "forwarded", "response": response.json()}
    return "Bot is running!"

# Set webhook
def set_webhook():
    url = f"https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/setWebhook"
    response = requests.post(url, data={"url": "https://your-railway-url.up.railway.app/"})
    print(response.json())

if __name__ == "__main__":
    set_webhook()
    app.run(host="0.0.0.0", port=5000)
