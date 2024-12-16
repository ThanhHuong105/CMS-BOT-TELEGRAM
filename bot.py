from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Hàm khởi động bot
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Chào bạn! Hãy gửi nội dung bài viết cùng file đính kèm (hình ảnh/video).")

# Hàm nhận nội dung và file đính kèm
def receive_content(update: Update, context: CallbackContext):
    # Lấy nội dung
    user_content = update.message.text
    # Kiểm tra tệp đính kèm (hình ảnh hoặc tài liệu)
    file = update.message.document or update.message.photo
    context.user_data['content'] = user_content
    context.user_data['file'] = file

    if file:
        update.message.reply_text("Bạn đã gửi nội dung và file! Tôi đang tạo bản xem trước.")
    else:
        update.message.reply_text("Bạn đã gửi nội dung, nhưng chưa có file đính kèm. Bạn có muốn gửi thêm không?")

# Hàm tạo bản xem trước
def preview(update: Update, context: CallbackContext):
    content = context.user_data.get('content', 'Không có nội dung')
    file = context.user_data.get('file', 'Không có tệp đính kèm')
    preview_message = f"📌 **Nội dung:**\n{content}\n\n🖼️ **File:** {file}"
    update.message.reply_text(preview_message)

# Khởi chạy bot
if __name__ == "__main__":
    # Token Telegram của bạn
    TOKEN = "7925656043:AAEbWFSv7_9WlWi78Hxw6Z5jigY2KgvAeg4"

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Gán lệnh và xử lý
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text | Filters.document | Filters.photo, receive_content))
    dp.add_handler(CommandHandler("preview", preview))

    # Bắt đầu bot
    updater.start_polling()
    updater.idle()
