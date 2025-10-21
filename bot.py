from telegram import Update, ChatMember
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    ChatMemberHandler,
    filters
)
import nest_asyncio
nest_asyncio.apply()
import os

# For local testing, you can hardcode your token:
# BOT_TOKEN = '8300808332:AAFpIwD_6wli3JKhrMu3elga8jF1jfIhdwM'

# for railway
import os

# BOT_TOKEN = os.environ['8300808332:AAFpIwD_6wli3JKhrMu3elga8jF1jfIhdwM']
BOT_TOKEN = os.environ['BOT_TOKEN']

if not BOT_TOKEN:
    print("❌ BOT_TOKEN is missing. Check Railway variables.")
    exit(1)


BANNED_WORDS = ['spam', 'scam', 'badword']

# Welcome new members
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.chat_member.new_chat_members:
        await update.effective_chat.send_message(
            f"👋 Welcome {member.full_name}! Please read the group rules with /rules."
        )

# Help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Available commands:\n/help - Show help\n/rules - Show group rules")

# Rules command
async def rules_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📜 Group Rules:\n1. Be respectful\n2. No spam\n3. Use English only")

# Filter banned words
async def filter_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    if any(word in text for word in BANNED_WORDS):
        await update.message.delete()
        await update.message.reply_text("⚠️ Message deleted: contains banned words.")

# Main function
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("rules", rules_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, filter_messages))
    app.add_handler(ChatMemberHandler(welcome, ChatMemberHandler.CHAT_MEMBER))

    print("✅ Bot is running...")
    await app.run_polling()

# Entry point
if __name__ == '__main__':
    import asyncio
    asyncio.run(main())