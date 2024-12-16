# Placeholder import for telegram modules due to environment restrictions
try:
    from telegram import Update, InputMediaPhoto, InputMediaVideo
    from telegram.ext import (ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters, ConversationHandler)
    from telegram.constants import ParseMode
except ModuleNotFoundError:
    print("\u26a0 Môi trường không hỗ trợ 'telegram'. Vui lòng kiểm tra việc cài đặt thư viện hoặc sử dụng môi trường khác.")
    Update = None
    ApplicationBuilder = None
    CommandHandler = None
    MessageHandler = None
    ContextTypes = None
    filters = None
    ConversationHandler = None

# Trạng thái của form
TITLE, CONTENT_IMAGE, COVER, HASHTAGS, CONFIRM = range(5)

# Khởi động form
data = {}

def placeholder_function():
    print("\u26a0 Bot không thể chạy do thiếu thư viện 'telegram'.")

async def start(update, context):
    if Update is None:
        placeholder_function()
        return ConversationHandler.END
    await update.message.reply_text(
        "\ud83d\udccb *Tạo bài viết mới*\n\ud83d\udcdd *Tiêu đề*: Hãy nhập tiêu đề bài viết",
        parse_mode=ParseMode.MARKDOWN)
    return TITLE

# Nhập tiêu đề
async def title(update, context):
    data['title'] = update.message.text
    await update.message.reply_text(
        "\ud83d\udcdd *Nội dung và hình ảnh/video chi tiết*:\n"
        "Gửi nội dung và ảnh/video kèm caption trong cùng một tin nhắn.",
        parse_mode=ParseMode.MARKDOWN)
    return CONTENT_IMAGE

# Nhập nội dung kèm hình/video
async def content_image(update, context):
    data['content'] = update.message.caption if update.message.caption else "(Không có nội dung)"
    if update.message.photo:
        data['content_image'] = update.message.photo[-1].file_id
    elif update.message.video:
        data['content_image'] = update.message.video.file_id
    else:
        data['content_image'] = None

    await update.message.reply_text(
        "\ud83d\uddbc *Hình ảnh/Video Cover*:\nGửi file hoặc paste link cho ảnh bìa",
        parse_mode=ParseMode.MARKDOWN)
    return COVER

# Nhập hình ảnh Cover
async def cover(update, context):
    if update.message.photo:
        data['cover'] = update.message.photo[-1].file_id
    elif update.message.video:
        data['cover'] = update.message.video.file_id
    else:
        data['cover'] = update.message.text

    await update.message.reply_text(
        "\ud83d\udd16 *Hashtags*:\nBot gợi ý: #example, #bot. Nhập hashtags của bạn (cách nhau bằng dấu phẩy)",
        parse_mode=ParseMode.MARKDOWN)
    return HASHTAGS

# Nhập Hashtags
async def hashtags(update, context):
    data['hashtags'] = update.message.text
    media = [
        InputMediaPhoto(data['content_image'], caption=f"\ud83d\udccb *Bản xem trước:*\n"
                         f"\ud83d\udcdd *Tiêu đề*: {data['title']}\n"
                         f"\ud83d\udcdd *Nội dung*: {data['content']}\n"
                         f"\ud83d\udd16 *Hashtags*: {data['hashtags']}",
                         parse_mode=ParseMode.MARKDOWN)
    ] if data['content_image'] else None

    if media:
        await update.message.reply_media_group(media=media)
    else:
        await update.message.reply_text(
            f"\ud83d\udccb *Bản xem trước:*\n\ud83d\udcdd *Tiêu đề*: {data['title']}\n"
            f"\ud83d\udcdd *Nội dung*: {data['content']}\n"
            f"\ud83d\udd16 *Hashtags*: {data['hashtags']}",
            parse_mode=ParseMode.MARKDOWN)

    await update.message.reply_text("\u2705 Gửi 'Xong' để xác nhận hoặc 'Hủy' để bỏ qua.")
    return CONFIRM

# Xác nhận
async def confirm(update, context):
    if update.message.text.lower() == "xong":
        await update.message.reply_text("\ud83c\udf89 Bài viết đã được tạo và lưu trữ! \ud83d\udcbe")
        # Gửi dữ liệu lên Google Sheets tại đây
    else:
        await update.message.reply_text("\u26a0 Bài viết đã bị hủy.")
    return ConversationHandler.END

# Hủy
async def cancel(update, context):
    await update.message.reply_text("\u26a0 Hủy tạo bài viết.")
    return ConversationHandler.END

# Khởi chạy bot
if __name__ == "__main__":
    if ApplicationBuilder is None:
        placeholder_function()
    else:
        TOKEN = "7925656043:AAEbWFSv7_9WlWi78Hxw6Z5jigY2KgvAeg4"
        app = ApplicationBuilder().token(TOKEN).build()

        # Conversation handler
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler("newpost", start)],
            states={
                TITLE: [MessageHandler(filters.TEXT, title)],
                CONTENT_IMAGE: [MessageHandler(filters.PHOTO | filters.VIDEO, content_image)],
                COVER: [MessageHandler(filters.PHOTO | filters.VIDEO | filters.TEXT, cover)],
                HASHTAGS: [MessageHandler(filters.TEXT, hashtags)],
                CONFIRM: [MessageHandler(filters.TEXT, confirm)],
            },
            fallbacks=[CommandHandler("cancel", cancel)],
        )

        app.add_handler(conv_handler)

        print("Bot dang chay...")
        app.run_polling()
