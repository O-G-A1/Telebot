from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    ChatMemberHandler,
    ConversationHandler,
    filters
)
import nest_asyncio
import os
nest_asyncio.apply()

# --- Bot Configuration ---
BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    print("❌ BOT_TOKEN is missing. Check Railway environment variables.")
    exit(1)

ADMIN_USER_ID = 7432554286  # 👈 Your Telegram numeric user ID

# --- Conversation States ---
ASK_EMAIL, ASK_PLATFORM, ASK_DESCRIPTION, ASK_EXTRA1, ASK_EXTRA2 = range(5)

# --- Banned Words List ---
BANNED_WORDS = [
    'spam', 'scam', 'fake', 'fraud', 'nude', 'porn', 'sex', 'hate',
    'terror', 'bomb', 'weapon', 'casino', 'betting', 'gamble', 'phishing'
]

# --- Welcome New Members ---
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.chat_member.new_chat_members:
        await update.effective_chat.send_message(
            f"👋 Welcome {member.full_name}! Please read the group rules with /rules."
        )

# --- /help Command ---
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📜 Rules", callback_data='rules')],
        [InlineKeyboardButton("🔗 Links", callback_data='links')],
        [InlineKeyboardButton("ℹ️ About", callback_data='about')],
        [InlineKeyboardButton("🚨 Report a Problem", callback_data='report_problem')]
    ]
    await update.message.reply_text("📘 Choose a help option:", reply_markup=InlineKeyboardMarkup(keyboard))

# --- /rules Command ---
async def rules_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("✅ I Accept", callback_data='accept_rules')],
        [InlineKeyboardButton("❓ Ask a Question", url="https://t.me/cryptochainnetwork")]
    ]
    rules_text = (
        "📜 *Group Rules*\n"
        "1️⃣ Be respectful to all members 🤝\n"
        "2️⃣ No spam, scams, or self-promotion 🚫📢\n"
        "3️⃣ Use English only 🇬🇧\n"
        "4️⃣ No hate speech or discrimination ❌\n"
        "5️⃣ Avoid adult or explicit content 🔞\n"
        "6️⃣ Report suspicious behavior 🕵️‍♂️"
    )
    await update.message.reply_text(rules_text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

# --- /start Command ---
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📜 View Rules", callback_data='rules')],
        [InlineKeyboardButton("ℹ️ About This Bot", callback_data='about')],
        [InlineKeyboardButton("🚨 Report a Problem", callback_data='report_problem')]
    ]
    await update.message.reply_text(
        f"Hi {update.effective_user.first_name}! I'm your group assistant bot 🤖.\nChoose an option below:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# --- /links Command ---
async def links_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📺 Join Channel", url="https://t.me/cryptochainnetwork")],
        [InlineKeyboardButton("🌐 Telegram", url="https://telegram.org")]
    ]
    await update.message.reply_text("🔗 Useful Links:", reply_markup=InlineKeyboardMarkup(keyboard))

# --- /about Command ---
async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("👨‍💻 Developer", url="https://t.me/gbenga")],
        [InlineKeyboardButton("📢 Updates Channel", url="https://t.me/cryptochainnetwork")]
    ]
    await update.message.reply_text(
        "🤖 This bot helps manage your group.\nIt welcomes new members, filters spam, and shares info.\nBuilt by Gbenga 💻",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# --- Handle Button Clicks ---
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "rules":
        await rules_command(update, context)

    elif query.data == "links":
        await links_command(update, context)

    elif query.data == "about":
        await about_command(update, context)

    elif query.data == "accept_rules":
        await query.edit_message_text("✅ Thank you! You may now participate in the group.")

    elif query.data == "report_problem":
        await query.message.reply_text("📧 Please enter your email address:")
        return ASK_EMAIL

# --- Conversation Flow ---
async def ask_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["email"] = update.message.text
    await update.message.reply_text("💼 What wallet or platform are you having issues with?")
    return ASK_PLATFORM

async def ask_platform(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["platform"] = update.message.text
    await update.message.reply_text("📝 Please describe your issue briefly:")
    return ASK_DESCRIPTION

async def ask_description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["description"] = update.message.text
    await update.message.reply_text("❓ Additional info (if any)? If none, type 'None':")
    return ASK_EXTRA1

async def ask_extra1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["extra1"] = update.message.text
    await update.message.reply_text("📌 Any screenshot or code reference? If none, type 'None':")
    return ASK_EXTRA2

async def ask_extra2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["extra2"] = update.message.text

    user = update.effective_user
    report = (
        "🚨 *New Problem Report Submitted*\n\n"
        f"👤 User: @{user.username or user.full_name}\n"
        f"📧 Email: {context.user_data.get('email')}\n"
        f"💼 Platform: {context.user_data.get('platform')}\n"
        f"📝 Description: {context.user_data.get('description')}\n"
        f"📄 Extra Info 1: {context.user_data.get('extra1')}\n"
        f"📄 Extra Info 2: {context.user_data.get('extra2')}"
    )

    await update.message.reply_text("✅ Thank you! Our team will review your report soon.")
    try:
        await context.bot.send_message(chat_id=ADMIN_USER_ID, text=report, parse_mode="Markdown")
    except Exception as e:
        print(f"❌ Error sending report to admin: {e}")

    return ConversationHandler.END

# --- Cancel ---
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Operation cancelled.")
    return ConversationHandler.END

# --- Message Filter ---
async def filter_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    if any(word in text for word in BANNED_WORDS):
        await update.message.delete()
        await update.message.reply_text("⚠️ Message deleted: contains banned words.")

# --- Main ---
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button_handler, pattern="^report_problem$")],
        states={
            ASK_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_email)],
            ASK_PLATFORM: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_platform)],
            ASK_DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_description)],
            ASK_EXTRA1: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_extra1)],
            ASK_EXTRA2: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_extra2)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("rules", rules_command))
    app.add_handler(CommandHandler("links", links_command))
    app.add_handler(CommandHandler("about", about_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, filter_messages))
    app.add_handler(ChatMemberHandler(welcome, ChatMemberHandler.CHAT_MEMBER))

    print("✅ Bot is running...")
    await app.run_polling()

# --- Entry Point ---
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())



# from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
# from telegram.ext import (
#     ApplicationBuilder,
#     CommandHandler,
#     MessageHandler,
#     CallbackQueryHandler,
#     ContextTypes,
#     ConversationHandler,
#     filters
# )
# import nest_asyncio
# import os

# nest_asyncio.apply()

# # --- Bot Configuration ---
# BOT_TOKEN = os.environ.get("BOT_TOKEN")
# if not BOT_TOKEN:
#     print("❌ BOT_TOKEN is missing. Check Railway environment variables.")
#     exit(1)

# ADMIN_USER_ID = 7432554286  # 👈 Your Telegram numeric user ID

# # --- Conversation States ---
# ASK_EMAIL, ASK_PLATFORM, ASK_DESCRIPTION, ASK_EXTRA1, ASK_EXTRA2 = range(5)

# # --- Banned Words List ---
# BANNED_WORDS = [
#     'spam', 'scam', 'fake', 'fraud', 'nude', 'porn', 'sex', 'hate',
#     'terror', 'bomb', 'weapon', 'casino', 'betting', 'gamble', 'phishing'
# ]

# # --- Welcome New Members ---
# async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     for member in update.message.new_chat_members:
#         await update.message.reply_text(
#             f"👋 Welcome {member.mention_html()}!\n"
#             f"Please read the group rules with /rules.",
#             parse_mode="HTML"
#         )

# # --- Goodbye for Leaving Members (optional) ---
# async def goodbye(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     if update.message.left_chat_member:
#         await update.message.reply_text(
#             f"👋 {update.message.left_chat_member.full_name} has left the group."
#         )

# # --- /help Command ---
# async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     keyboard = [
#         [InlineKeyboardButton("📜 Rules", callback_data='rules')],
#         [InlineKeyboardButton("🔗 Links", callback_data='links')],
#         [InlineKeyboardButton("ℹ️ About", callback_data='about')],
#         [InlineKeyboardButton("🚨 Report a Problem", callback_data='report_problem')]
#     ]
#     await update.message.reply_text("📘 Choose a help option:", reply_markup=InlineKeyboardMarkup(keyboard))

# # --- /rules Command ---
# async def rules_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     keyboard = [
#         [InlineKeyboardButton("✅ I Accept", callback_data='accept_rules')],
#         [InlineKeyboardButton("❓ Ask a Question", url="https://t.me/cryptochainnetwork")]
#     ]
#     rules_text = (
#         "📜 *Group Rules*\n"
#         "1️⃣ Be respectful to all members 🤝\n"
#         "2️⃣ No spam, scams, or self-promotion 🚫📢\n"
#         "3️⃣ Use English only 🇬🇧\n"
#         "4️⃣ No hate speech or discrimination ❌\n"
#         "5️⃣ Avoid adult or explicit content 🔞\n"
#         "6️⃣ Report suspicious behavior 🕵️‍♂️"
#     )
#     await update.message.reply_text(rules_text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

# # --- /start Command ---
# async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     keyboard = [
#         [InlineKeyboardButton("📜 View Rules", callback_data='rules')],
#         [InlineKeyboardButton("ℹ️ About This Bot", callback_data='about')],
#         [InlineKeyboardButton("🚨 Report a Problem", callback_data='report_problem')]
#     ]
#     await update.message.reply_text(
#         f"Hi {update.effective_user.first_name}! I'm your group assistant bot 🤖.\nChoose an option below:",
#         reply_markup=InlineKeyboardMarkup(keyboard)
#     )

# # --- /links Command ---
# async def links_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     keyboard = [
#         [InlineKeyboardButton("📺 Join Channel", url="https://t.me/cryptochainnetwork")],
#         [InlineKeyboardButton("🌐 Telegram", url="https://telegram.org")]
#     ]
#     await update.message.reply_text("🔗 Useful Links:", reply_markup=InlineKeyboardMarkup(keyboard))

# # --- /about Command ---
# async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     keyboard = [
#         [InlineKeyboardButton("👨‍💻 Developer", url="https://t.me/gbenga")],
#         [InlineKeyboardButton("📢 Updates Channel", url="https://t.me/cryptochainnetwork")]
#     ]
#     await update.message.reply_text(
#         "🤖 This bot helps manage your group.\nIt welcomes new members, filters spam, and shares info.\nBuilt by Gbenga 💻",
#         reply_markup=InlineKeyboardMarkup(keyboard)
#     )

# # --- Handle Button Clicks ---
# async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     query = update.callback_query
#     await query.answer()

#     if query.data == "rules":
#         await rules_command(update, context)

#     elif query.data == "links":
#         await links_command(update, context)

#     elif query.data == "about":
#         await about_command(update, context)

#     elif query.data == "accept_rules":
#         await query.edit_message_text("✅ Thank you! You may now participate in the group.")

#     elif query.data == "report_problem":
#         await query.message.reply_text("📧 Please enter your email address:")
#         return ASK_EMAIL

# # --- Conversation Flow ---
# async def ask_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     context.user_data["email"] = update.message.text
#     await update.message.reply_text("💼 What wallet or platform are you having issues with?")
#     return ASK_PLATFORM

# async def ask_platform(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     context.user_data["platform"] = update.message.text
#     await update.message.reply_text("📝 Please describe your issue briefly:")
#     return ASK_DESCRIPTION

# async def ask_description(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     context.user_data["description"] = update.message.text
#     await update.message.reply_text("❓ Additional info (if any)? If none, type 'None':")
#     return ASK_EXTRA1

# async def ask_extra1(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     context.user_data["extra1"] = update.message.text
#     await update.message.reply_text("📌 Any screenshot or code reference? If none, type 'None':")
#     return ASK_EXTRA2

# async def ask_extra2(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     context.user_data["extra2"] = update.message.text

#     user = update.effective_user
#     report = (
#         "🚨 *New Problem Report Submitted*\n\n"
#         f"👤 User: @{user.username or user.full_name}\n"
#         f"📧 Email: {context.user_data.get('email')}\n"
#         f"💼 Platform: {context.user_data.get('platform')}\n"
#         f"📝 Description: {context.user_data.get('description')}\n"
#         f"📄 Extra Info 1: {context.user_data.get('extra1')}\n"
#         f"📄 Extra Info 2: {context.user_data.get('extra2')}"
#     )

#     await update.message.reply_text("✅ Thank you! Our team will review your report soon.")
#     try:
#         await context.bot.send_message(chat_id=ADMIN_USER_ID, text=report, parse_mode="Markdown")
#     except Exception as e:
#         print(f"❌ Error sending report to admin: {e}")

#     return ConversationHandler.END

# # --- Cancel ---
# async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply
