import csv
import os
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from telegram import Update

BOT_TOKEN = "8036268612:AAGSvC47SxzNw_lsmUHGYjuiGFoTaRLaEfk"
CSV_FILE = "file_ids.csv"

# Ensure the CSV file exists and has headers
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["file_name", "file_type", "file_id"])

async def log_file_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    row = []

    if msg.document:
        file_name = msg.document.file_name
        file_id = msg.document.file_id
        file_type = "document"
        row = [file_name, file_type, file_id]
        print(f"📄 Document: {file_name} | File ID: {file_id}")

    elif msg.video:
        file_name = msg.video.file_name or "unnamed_video"
        file_id = msg.video.file_id
        file_type = "video"
        row = [file_name, file_type, file_id]
        print(f"🎥 Video: {file_name} | File ID: {file_id}")

    else:
        print("❌ Unsupported file type")
        return

    # Append the row to the CSV file
    with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(row)
        print("✅ File ID saved to CSV.")

# Build and run the bot
app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.ALL, log_file_id))
print("🤖 Bot is running... waiting for uploads.")
app.run_polling()
