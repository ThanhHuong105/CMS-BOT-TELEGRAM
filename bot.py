from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
)

# Hàm khởi động bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Chào bạn! Hãy gửi nội dung bài viết cùng file đính kèm (hình ảnh/video).")

# Hàm nhận nội dung và file đính kèm
async def receive_content(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_content = update.message.text
    file = update.message.document or update.message.photo

    context.user_data['content'] = user_content
    context.user_data['file'] = file

    if file:
        await update.message.reply_text("Bạn đã gửi nội dung và file! Tôi đang tạo bản xem trước.")
    else:
        await update.message.reply_text("Bạn đã gửi nội dung, nhưng chưa có file đính kèm. Bạn có muốn gửi thêm không?")

# Hàm tạo bản xem trước
async def preview(update: Update, context: ContextTypes.DEFAULT_TYPE):
    content = context.user_data.get('content', 'Không có nội dung')
    file = context.user_data.get('file', 'Không có tệp đính kèm')

    preview_message = f"📌 **Nội dung:**\n{content}\n\n🖼️ **File:** {file}"
    await update.message.reply_text(preview_message)

# Khởi chạy bot
if __name__ == "__main__":
    TOKEN = "7925656043:AAEbWFSv7_9WlWi78Hxw6Z5jigY2KgvAeg4"

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT | filters.Document.ALL | filters.PHOTO, receive_content))
    app.add_handler(CommandHandler("preview", preview))

    print("Bot đang chạy...")
    app.run_polling()
