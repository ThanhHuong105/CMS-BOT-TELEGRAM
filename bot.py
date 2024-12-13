import os
from datetime import datetime
from flask import Flask, request, jsonify
import requests
import re

app = Flask(__name__)

# === TELEGRAM BOT CONFIGURATION ===
BOT_TOKEN = "7925656043:AAEbWFSv7_9WlWi78Hxw6Z5jigY2KgvAeg4"
if not BOT_TOKEN:
    raise ValueError("Bot token is missing. Please provide a valid BOT_TOKEN.")

TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/"

# === BOT STATES ===
STATE = {}
FILE_STORAGE = {}

@app.route(f"/webhook/{BOT_TOKEN}", methods=['POST'])
def webhook():
    try:
        data = request.get_json()
        if not data or "message" not in data:
            return jsonify({"status": "ignored"}), 200

        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        if chat_id not in STATE:
            STATE[chat_id] = {"step": "TITLE", "placeholders": []}

        step = STATE[chat_id]["step"]

        if step == "TITLE":
            STATE[chat_id]["title"] = text
            STATE[chat_id]["step"] = "CONTENT"
            send_message(chat_id, "Hãy nhập nội dung bài viết của bạn. Nếu muốn chèn hình ảnh/video, hãy sử dụng các placeholder như [Ảnh1] hoặc [Video1]:")

        elif step == "CONTENT":
            STATE[chat_id]["content"] = text
            placeholders = extract_placeholders(text)
            STATE[chat_id]["placeholders"] = placeholders

            if placeholders:
                placeholder = placeholders.pop(0)
                STATE[chat_id]["step"] = "PLACEHOLDER"
                STATE[chat_id]["current_placeholder"] = placeholder
                send_message(chat_id, f"Hãy gửi hình ảnh hoặc video cho {placeholder}:")
            else:
                STATE[chat_id]["step"] = "TAGS"
                send_message(chat_id, "Hãy nhập các tag (nếu có), hoặc gõ 'bỏ qua' nếu không cần:")

        elif step == "PLACEHOLDER":
            placeholder = STATE[chat_id].get("current_placeholder")
            if "photo" in data["message"]:
                file_id = data["message"]["photo"][-1]["file_id"]
                FILE_STORAGE[placeholder] = file_id
            elif "video" in data["message"]:
                file_id = data["message"]["video"]["file_id"]
                FILE_STORAGE[placeholder] = file_id
            else:
                send_message(chat_id, f"Không tìm thấy file cho {placeholder}. Hãy gửi lại hình ảnh hoặc video.")
                return jsonify({"status": "waiting for file"}), 200

            placeholders = STATE[chat_id]["placeholders"]
            if placeholders:
                next_placeholder = placeholders.pop(0)
                STATE[chat_id]["current_placeholder"] = next_placeholder
                send_message(chat_id, f"Hãy gửi hình ảnh hoặc video cho {next_placeholder}:")
            else:
                STATE[chat_id]["step"] = "TAGS"
                send_message(chat_id, "Hãy nhập các tag (nếu có), hoặc gõ 'bỏ qua' nếu không cần:")

        elif step == "TAGS":
            if text.lower() != "bỏ qua":
                STATE[chat_id]["tags"] = text
            else:
                STATE[chat_id]["tags"] = ""

            STATE[chat_id]["step"] = "CHANNEL"
            send_message(chat_id, "Hãy chọn kênh để đăng bài:\n1. Telegram\n2. Facebook")

        elif step == "CHANNEL":
            STATE[chat_id]["channel"] = "Telegram" if text == "1" else "Facebook"

            # Hiển thị bài viết demo
            demo_message = create_demo_message(STATE[chat_id])
            send_message(chat_id, demo_message, parse_mode="Markdown")

            STATE[chat_id]["step"] = "CONFIRMATION"
            send_message(chat_id, "Bạn có muốn đăng bài này không? (Yes/No)")

        elif step == "CONFIRMATION":
            if text.lower() == "yes":
                send_message(chat_id, "Bài viết của bạn đang được đăng...")
                post_content(STATE[chat_id])
                del STATE[chat_id]
            else:
                send_message(chat_id, "Bạn đã hủy bài viết. Nếu muốn, hãy bắt đầu lại bằng cách nhập /start.")
                del STATE[chat_id]

        return jsonify({"status": "success"}), 200
    except Exception as e:
        print(f"Error in webhook handling: {e}")
        return jsonify({"error": str(e)}), 500

def send_message(chat_id, text, parse_mode=None):
    url = TELEGRAM_API_URL + "sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    if parse_mode:
        payload["parse_mode"] = parse_mode

    try:
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            print(f"Error sending message: {response.status_code}, {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending message: {e}")

def extract_placeholders(content):
    return re.findall(r'\[(Ảnh|Video)\d+\]', content)

def create_demo_message(state):
    content = state.get("content", "")
    for placeholder, file_id in FILE_STORAGE.items():
        content = content.replace(placeholder, f"<File {file_id}>")

    demo = (
        f"📝 **Bản nháp bài viết của bạn:**\n\n"
        f"**Tiêu đề:** {state.get('title', '')}\n"
        f"**Nội dung:**\n{content}\n"
        f"**Tags:** {state.get('tags', 'Không có')}\n"
        f"**Sẽ đăng trên:** {state.get('channel', 'Không rõ')}\n"
    )
    return demo

def post_content(state):
    # TODO: Xử lý đăng bài lên Telegram hoặc Facebook
    print("Đăng bài với nội dung:", state)

if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 5000))
    RAILWAY_STATIC_URL = os.environ.get("RAILWAY_STATIC_URL")
    if not RAILWAY_STATIC_URL:
        raise ValueError("RAILWAY_STATIC_URL is not set. Ensure Railway provides the correct URL.")

    webhook_url = f"https://{RAILWAY_STATIC_URL}/webhook/{BOT_TOKEN}"
    print(f"Setting Telegram webhook to {webhook_url}...")
    try:
        webhook_response = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url={webhook_url}")
        if webhook_response.status_code == 200:
            print("Webhook set successfully.")
        else:
            print(f"Failed to set webhook: {webhook_response.status_code}, {webhook_response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Webhook setup failed: {e}")

    print("Starting Flask app...")
    try:
        app.run(host="0.0.0.0", port=PORT, debug=True)
    except Exception as e:
        print(f"Critical error: {e}")
