# import asyncio
# import csv
# from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
# from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# BOT_TOKEN = "8036268612:AAGSvC47SxzNw_lsmUHGYjuiGFoTaRLaEfk"
# CSV_FILE = "file_ids.csv"
# USER_PROGRESS = {}

# # Load video file_ids from CSV
# def load_videos_from_csv():
#     videos = []
#     with open(CSV_FILE, newline='', encoding='utf-8') as file:
#         reader = csv.DictReader(file)
#         for row in reader:
#             if row["file_type"] in ["video", "document"]:
#                 videos.append({
#                     "name": row["file_name"],
#                     "file_id": row["file_id"]
#                 })
#     return videos

# VIDEO_LIST = load_videos_from_csv()

# # /start command
# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     print("📩 /start received")
#     keyboard = [[InlineKeyboardButton("🎬 Get Video", callback_data="get_video")]]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     await update.message.reply_text("📚 Click below to get the next lecture video:", reply_markup=reply_markup)

# # Handle "Get Video" button click
# async def handle_get_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     query = update.callback_query
#     await query.answer()
#     user_id = query.from_user.id

#     # Get user progress or start from 0
#     index = USER_PROGRESS.get(user_id, 0)

#     if index < len(VIDEO_LIST):
#         video = VIDEO_LIST[index]
#         sent = await query.message.reply_video(video=video["file_id"], caption=f"🎥 {video['name']}")
#         chat_id = sent.chat.id
#         message_id = sent.message_id

#         # Schedule deletion (2 hours = 7200 sec), set to 10 for testing
#         asyncio.create_task(delete_after_delay(context, chat_id, message_id, delay=7200))

#         USER_PROGRESS[user_id] = index + 1  # Move to next video
#     else:
#         await query.message.reply_text("✅ You’ve watched all available videos!")

# # Delete message after a delay
# async def delete_after_delay(context: ContextTypes.DEFAULT_TYPE, chat_id: int, message_id: int, delay: int):
#     try:
#         await asyncio.sleep(delay)
#         await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
#         print(f"🗑️ Deleted message {message_id} in chat {chat_id}")
#     except Exception as e:
#         print(f"⚠️ Error deleting message: {e}")

# # Run the bot
# def main():
#     app = ApplicationBuilder().token(BOT_TOKEN).build()
#     app.add_handler(CommandHandler("start", start))
#     app.add_handler(CallbackQueryHandler(handle_get_video, pattern="get_video"))
#     print("🤖 Bot is running...")
#     app.run_polling()

# if __name__ == "__main__":
#     main()

# import asyncio
# import csv
# from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
# from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
# from telegram import ReplyKeyboardMarkup

# BOT_TOKEN = "8036268612:AAGSvC47SxzNw_lsmUHGYjuiGFoTaRLaEfk"
# CSV_FILE = "file_ids.csv"
# USER_PROGRESS = {}  # { user_id: [file_ids] }

# # Load video file_ids from CSV
# def load_videos_from_csv():
#     videos = []
#     with open(CSV_FILE, newline='', encoding='utf-8') as file:
#         reader = csv.DictReader(file)
#         for row in reader:
#             if row["file_type"] in ["video", "document"]:
#                 videos.append({
#                     "name": row["file_name"],
#                     "file_id": row["file_id"]
#                 })
#     return videos

# VIDEO_LIST = load_videos_from_csv()

# # /start command
# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     print("📩 /start received")
#     keyboard = [[InlineKeyboardButton("🎬 Get Video", callback_data="get_video")]]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     await update.message.reply_text("📚 Click below to get the next lecture video:", reply_markup=reply_markup)

# # Handle "Get Video" button click
# async def handle_get_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     query = update.callback_query
#     await query.answer()
#     user_id = query.from_user.id

#     # Get list of watched video_ids for the user
#     watched = USER_PROGRESS.get(user_id, [])

#     # Find first unwatched video
#     next_video = None
#     for video in VIDEO_LIST:
#         if video["file_id"] not in watched:
#             next_video = video
#             break

#     if next_video:
#         sent = await query.message.reply_video(
#             video=next_video["file_id"],
#             caption=f"🎥 {next_video['name']}"
#         )

#         # Schedule deletion (2 hours = 7200 sec), use 10 for testing
#         asyncio.create_task(delete_after_delay(context, sent.chat.id, sent.message_id, delay=7200))

#         # Update user progress
#         watched.append(next_video["file_id"])
#         USER_PROGRESS[user_id] = watched
#     else:
#         await query.message.reply_text("✅ You’ve watched all available videos!")

# # Delete message after delay
# async def delete_after_delay(context: ContextTypes.DEFAULT_TYPE, chat_id: int, message_id: int, delay: int):
#     try:
#         await asyncio.sleep(delay)
#         await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
#         print(f"🗑️ Deleted message {message_id} in chat {chat_id}")
#     except Exception as e:
#         print(f"⚠️ Error deleting message: {e}")

# # Run the bot
# def main():
#     app = ApplicationBuilder().token(BOT_TOKEN).build()
#     app.add_handler(CommandHandler("start", start))
#     app.add_handler(CallbackQueryHandler(handle_get_video, pattern="get_video"))
#     print("🤖 Bot is running...")
#     app.run_polling()

# if __name__ == "__main__":
#     main()


import asyncio
import csv
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

BOT_TOKEN = "8036268612:AAGSvC47SxzNw_lsmUHGYjuiGFoTaRLaEfk"
CSV_FILE = "file_ids.csv"
USER_PROGRESS = {}  # { user_id: [file_ids] }

# Load video file_ids from CSV
def load_videos_from_csv():
    videos = []
    with open(CSV_FILE, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["file_type"] in ["video", "document"]:
                videos.append({
                    "name": row["file_name"],
                    "file_id": row["file_id"]
                })
    return videos

VIDEO_LIST = load_videos_from_csv()

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("📩 /start received")
    reply_keyboard = [["🎬 Get Video"]]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "📚 Use the button below to get your next lecture video:",
        reply_markup=markup
    )

# Handle "🎬 Get Video" message
async def handle_get_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    # Get list of watched video_ids for the user
    watched = USER_PROGRESS.get(user_id, [])

    # Find first unwatched video
    next_video = None
    for video in VIDEO_LIST:
        if video["file_id"] not in watched:
            next_video = video
            break

    if next_video:
        sent = await update.message.reply_video(
            video=next_video["file_id"],
            caption=f"🎥 {next_video['name']}"
        )

        # Schedule deletion (2 hours = 7200 sec), set to 10 for testing
        asyncio.create_task(delete_after_delay(context, sent.chat.id, sent.message_id, delay=7200))

        # Update user progress
        watched.append(next_video["file_id"])
        USER_PROGRESS[user_id] = watched
    else:
        await update.message.reply_text("✅ You’ve watched all available videos!")

# Delete message after delay
async def delete_after_delay(context: ContextTypes.DEFAULT_TYPE, chat_id: int, message_id: int, delay: int):
    try:
        await asyncio.sleep(delay)
        await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
        print(f"🗑️ Deleted message {message_id} in chat {chat_id}")
    except Exception as e:
        print(f"⚠️ Error deleting message: {e}")

# Run the bot
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("^🎬 Get Video$"), handle_get_video))
    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
