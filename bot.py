from telegram import Update, InputMediaPhoto, InputMediaVideo
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes,
    filters, ConversationHandler
)
from telegram.constants import ParseMode

# Trạng thái của form
TITLE, CONTENT_IMAGE, HASHTAGS, CONFIRM = range(4)

# Khởi động form
data = {}

# Bắt đầu form
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("Bot đã nhận lệnh /start.")  # Log xác nhận
    await update.message.reply_text(
        "\ud83d\udccb *Tạo bài viết mới*\n\ud83d\udcdd *Tiêu đề*: Hãy nhập tiêu đề bài viết.",
        parse_mode=ParseMode.MARKDOWN
    )
    return TITLE

# Nhập tiêu đề
async def title(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data['title'] = update.message.text
    await update.message.reply_text(
        "\ud83d\udcdd *Nội dung và ảnh/video chi tiết*:\n"
        "Hãy gửi nội dung và kèm ảnh/video trong cùng một tin nhắn (caption).",
        parse_mode=ParseMode.MARKDOWN
    )
    return CONTENT_IMAGE

# Nhập nội dung kèm ảnh/video
async def content_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data['content'] = update.message.caption if update.message.caption else "(Không có nội dung)"
    if update.message.photo:
        data['media'] = InputMediaPhoto(update.message.photo[-1].file_id, caption=data['content'])
    elif update.message.video:
        data['media'] = InputMediaVideo(update.message.video.file_id, caption=data['content'])
    else:
        await update.message.reply_text("\u26a0 Vui lòng gửi ảnh hoặc video kèm nội dung.")
        return CONTENT_IMAGE

    await update.message.reply_text(
        "\ud83d\udd16 *Hashtags*: Nhập hashtags của bạn (cách nhau bằng dấu phẩy).",
        parse_mode=ParseMode.MARKDOWN
    )
    return HASHTAGS

# Nhập hashtags
async def hashtags(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data['hashtags'] = update.message.text
    if 'media' in data:
        caption = f"\ud83d\udccb *Bản xem trước:*\n\ud83d\udcdd *Tiêu đề*: {data['title']}\n\ud83d\udd16 *Hashtags*: {data['hashtags']}"
        data['media'].caption = caption
        await update.message.reply_media_group([data['media']])
    else:
        await update.message.reply_text("\u26a0 Lỗi khi xử lý nội dung. Vui lòng thử lại!")

    await update.message.reply_text("\u2705 Gửi 'Xong' để xác nhận hoặc 'Hủy' để bỏ qua.")
    return CONFIRM

# Xác nhận lưu bài viết
async def confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text.lower() == "xong":
        await update.message.reply_text("\ud83c\udf89 Bài viết đã được lưu trữ thành công! \ud83d\udcbe")
    else:
        await update.message.reply_text("\u26a0 Bài viết đã bị hủy.")
    return ConversationHandler.END

# Hủy thao tác
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("\u26a0 Hủy tạo bài viết.")
    return ConversationHandler.END

# Khởi chạy bot
if __name__ == "__main__":
    TOKEN = "7925656043:AAEbWFSv7_9WlWi78Hxw6Z5jigY2KgvAeg4"
    app = ApplicationBuilder().token(TOKEN).build()

    # Conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            TITLE: [MessageHandler(filters.TEXT, title)],
            CONTENT_IMAGE: [MessageHandler(filters.PHOTO | filters.VIDEO, content_image)],
            HASHTAGS: [MessageHandler(filters.TEXT, hashtags)],
            CONFIRM: [MessageHandler(filters.TEXT, confirm)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)

    print("Bot đang chạy... Hãy gửi lệnh /start để bắt đầu.")
    app.run_polling()
