# from telegram import Update, ChatMember, InlineKeyboardButton, InlineKeyboardMarkup
# from telegram.ext import (
#     ApplicationBuilder,
#     CommandHandler,
#     MessageHandler,
#     CallbackQueryHandler,
#     ContextTypes,
#     ChatMemberHandler,
#     filters
# )
# import nest_asyncio
# nest_asyncio.apply()
# import os

# BOT_TOKEN = os.environ['BOT_TOKEN']
# if not BOT_TOKEN:
#     print("❌ BOT_TOKEN is missing. Check Railway variables.")
#     exit(1)

# BANNED_WORDS = [
#     'spam', 'scam', 'badword', 'fake', 'fraud', 'click here',
#     'free money', 'nude', 'xxx', 'porn', 'sex', 'hate', 'racist',
#     'terror', 'kill', 'bomb', 'attack', 'drugs', 'weapon', 'casino',
#     'betting', 'gamble', 'credit card', 'make money fast', 'urgent',
#     'viagra', 'escort', 'adult', 'explicit', 'nsfw', 'malware',
#     'phishing', 'get rich quick'
# ]

# # Welcome new members
# async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     for member in update.chat_member.new_chat_members:
#         await update.effective_chat.send_message(
#             f"👋 Welcome {member.full_name}! Please read the group rules with /rules."
#         )

# # Help command
# async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     keyboard = [
#         [InlineKeyboardButton("📜 Rules", callback_data='rules')],
#         [InlineKeyboardButton("🔗 Links", callback_data='links')],
#         [InlineKeyboardButton("ℹ️ About", callback_data='about')],
#         [InlineKeyboardButton("🪙 Crypto Portal", url="https://cryptoportal.byethost8.com")]
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     await update.message.reply_text("📘 Choose a help option:", reply_markup=reply_markup)

# # Rules command
# async def rules_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     keyboard = [
#         [InlineKeyboardButton("✅ I Accept", callback_data='accept_rules')],
#         [InlineKeyboardButton("❓ Ask a Question", url="https://t.me/cryptochainnetwork")]
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     await update.message.reply_text(
#         "📜 *Group Rules*\n"
#         "1️⃣ Be respectful to all members 🤝\n"
#         "2️⃣ No spam, scams, or self-promotion 🚫📢\n"
#         "3️⃣ Use English only in discussions 🇬🇧🗣️\n"
#         "4️⃣ No hate speech, racism, or discrimination ❌🧠\n"
#         "5️⃣ Avoid sharing explicit or adult content 🔞🚫\n"
#         "6️⃣ Do not post fake news or misleading info 📰⚠️\n"
#         "7️⃣ Keep conversations on-topic 📌🗨️\n"
#         "8️⃣ No unsolicited private messages to members 📵📩\n"
#         "9️⃣ Report suspicious behavior to admins 🕵️‍♂️📣\n"
#         "🔟 Admin decisions are final — follow instructions 👮✅",
#         reply_markup=reply_markup,
#         parse_mode="Markdown"
#     )

# # Filter banned words
# async def filter_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     text = update.message.text.lower()
#     if any(word in text for word in BANNED_WORDS):
#         await update.message.delete()
#         await update.message.reply_text("⚠️ Message deleted: contains banned words.")

# # Start command with buttons
# async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     keyboard = [
#         [InlineKeyboardButton("📜 View Rules", callback_data='rules')],
#         [InlineKeyboardButton("ℹ️ About This Bot", callback_data='about')],
#         [InlineKeyboardButton("🪙 Crypto Portal", url="https://cryptoportal.byethost8.com")],
#         [InlineKeyboardButton("🌐 Telegram", url="https://telegram.org")],
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     await update.message.reply_text(
#         f"Hi {update.effective_user.first_name}! I'm your group assistant bot 🤖.\nChoose an option below:",
#         reply_markup=reply_markup
#     )

# # Links command
# async def links_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     keyboard = [
#         [InlineKeyboardButton("🌐 Telegram", url="https://telegram.org")],
#         [InlineKeyboardButton("📺 Join Channel", url="https://t.me/cryptochainnetwork")],
#         [InlineKeyboardButton("🪙 Crypto Portal", url="https://cryptoportal.byethost8.com")]
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     await update.message.reply_text("🔗 Useful Links:", reply_markup=reply_markup)

# # About command
# async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     keyboard = [
#         [InlineKeyboardButton("👨‍💻 Developer", url="https://t.me/gbenga")],
#         [InlineKeyboardButton("📢 Updates Channel", url="https://t.me/cryptochainnetwork")]
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     await update.message.reply_text(
#         "🤖 This bot helps manage your group.\nIt welcomes new members, filters spam, and shares useful info.\nBuilt by Gbenga 💻",
#         reply_markup=reply_markup
#     )

# # Handle button callbacks
# async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     query = update.callback_query
#     await query.answer()

#     if query.data == 'rules':
#         await query.edit_message_text(
#             "📜 *Group Rules*\n"
#             "1️⃣ Be respectful to all members 🤝\n"
#             "2️⃣ No spam, scams, or self-promotion 🚫📢\n"
#             "3️⃣ Use English only in discussions 🇬🇧🗣️\n"
#             "4️⃣ No hate speech, racism, or discrimination ❌🧠\n"
#             "5️⃣ Avoid sharing explicit or adult content 🔞🚫\n"
#             "6️⃣ Do not post fake news or misleading info 📰⚠️\n"
#             "7️⃣ Keep conversations on-topic 📌🗨️\n"
#             "8️⃣ No unsolicited private messages to members 📵📩\n"
#             "9️⃣ Report suspicious behavior to admins 🕵️‍♂️📣\n"
#             "🔟 Admin decisions are final — follow instructions 👮✅",
#             parse_mode="Markdown"
#         )

#     elif query.data == 'links':
#         await query.message.reply_text(
#             "🔗 Useful Links:",
#             reply_markup=InlineKeyboardMarkup([
#                 [InlineKeyboardButton("🌐 Telegram", url="https://telegram.org")],
#                 [InlineKeyboardButton("📺 Join Channel", url="https://t.me/cryptochainnetwork")],
#                 [InlineKeyboardButton("🪙 Crypto Portal", url="https://cryptoportal.byethost8.com")]
#             ])
#         )

#     elif query.data == 'about':
#         await query.message.reply_text(
#             "🤖 This bot helps manage your group.\n"
#             "It welcomes new members, filters spam, and shares useful info.\n"
#             "Built by Gbenga 💻",
#             reply_markup=InlineKeyboardMarkup([
#                 [InlineKeyboardButton("👨‍💻 Developer", url="https://t.me/adeboye_99")],
#                 [InlineKeyboardButton("📢 Updates Channel", url="https://t.me/cryptochainnetwork")]
#             ])
#         )

#     elif query.data == 'accept_rules':
#         await query.edit_message_text("✅ Thank you! You may now participate in the group.")

# # Main function
# async def main():
#     app = ApplicationBuilder().token(BOT_TOKEN).build()

#     app.add_handler(CommandHandler("start", start_command))
#     app.add_handler(CommandHandler("help", help_command))
#     app.add_handler(CommandHandler("rules", rules_command))
#     app.add_handler(CommandHandler("links", links_command))
#     app.add_handler(CommandHandler("about", about_command))
#     app.add_handler(CallbackQueryHandler(button_handler))
#     app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, filter_messages))
#     app.add_handler(ChatMemberHandler(welcome, ChatMemberHandler.CHAT_MEMBER))

#     print("✅ Bot is running...")
#     await app.run_polling()

# # Entry point
# if __name__ == '__main__':
#     import asyncio
#     asyncio.run(main())

from telegram import Update, ChatMember, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    ChatMemberHandler,
    filters,
    ConversationHandler
)
import nest_asyncio
nest_asyncio.apply()
import os

BOT_TOKEN = os.environ['BOT_TOKEN']
if not BOT_TOKEN:
    print("❌ BOT_TOKEN is missing. Check Railway variables.")
    exit(1)

BANNED_WORDS = [
    'spam', 'scam', 'badword', 'fake', 'fraud', 'click here',
    'free money', 'nude', 'xxx', 'porn', 'sex', 'hate', 'racist',
    'terror', 'kill', 'bomb', 'attack', 'drugs', 'weapon', 'casino',
    'betting', 'gamble', 'credit card', 'make money fast', 'urgent',
    'viagra', 'escort', 'adult', 'explicit', 'nsfw', 'malware',
    'phishing', 'get rich quick'
]

# === States for conversation ===
ASK_EMAIL, ASK_ISSUE, ASK_Q1, ASK_Q2, ASK_Q3 = range(5)

# Welcome new members
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.chat_member.new_chat_members:
        await update.effective_chat.send_message(
            f"👋 Welcome {member.full_name}! Please read the group rules with /rules."
        )

# Help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📜 Rules", callback_data='rules')],
        [InlineKeyboardButton("🔗 Links", callback_data='links')],
        [InlineKeyboardButton("ℹ️ About", callback_data='about')],
        [InlineKeyboardButton("🪙 Crypto Portal", url="https://cryptoportal.byethost8.com")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("📘 Choose a help option:", reply_markup=reply_markup)

# Rules command
async def rules_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("✅ I Accept", callback_data='accept_rules')],
        [InlineKeyboardButton("❓ Ask a Question", url="https://t.me/cryptochainnetwork")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "📜 *Group Rules*\n"
        "1️⃣ Be respectful to all members 🤝\n"
        "2️⃣ No spam, scams, or self-promotion 🚫📢\n"
        "3️⃣ Use English only in discussions 🇬🇧🗣️\n"
        "4️⃣ No hate speech, racism, or discrimination ❌🧠\n"
        "5️⃣ Avoid sharing explicit or adult content 🔞🚫\n"
        "6️⃣ Do not post fake news or misleading info 📰⚠️\n"
        "7️⃣ Keep conversations on-topic 📌🗨️\n"
        "8️⃣ No unsolicited private messages to members 📵📩\n"
        "9️⃣ Report suspicious behavior to admins 🕵️‍♂️📣\n"
        "🔟 Admin decisions are final — follow instructions 👮✅",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# Filter banned words
async def filter_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    if any(word in text for word in BANNED_WORDS):
        await update.message.delete()
        await update.message.reply_text("⚠️ Message deleted: contains banned words.")

# Start command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📜 View Rules", callback_data='rules')],
        [InlineKeyboardButton("ℹ️ About This Bot", callback_data='about')],
        [InlineKeyboardButton("🪙 Crypto Portal", url="https://cryptoportal.byethost8.com")],
        [InlineKeyboardButton("🌐 Telegram", url="https://telegram.org")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"Hi {update.effective_user.first_name}! I'm your group assistant bot 🤖.\nChoose an option below:",
        reply_markup=reply_markup
    )

# Links command
async def links_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🌐 Telegram", url="https://telegram.org")],
        [InlineKeyboardButton("📺 Join Channel", url="https://t.me/cryptochainnetwork")],
        [InlineKeyboardButton("🪙 Crypto Portal", url="https://cryptoportal.byethost8.com")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🔗 Useful Links:", reply_markup=reply_markup)

# About command
async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("👨‍💻 Developer", url="https://t.me/gbenga")],
        [InlineKeyboardButton("📢 Updates Channel", url="https://t.me/cryptochainnetwork")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🤖 This bot helps manage your group.\nIt welcomes new members, filters spam, and assists users.\nBuilt by Gbenga 💻",
        reply_markup=reply_markup
    )

# Handle button callbacks
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'rules':
        await query.edit_message_text(
            "📜 *Group Rules*\n"
            "1️⃣ Be respectful to all members 🤝\n"
            "2️⃣ No spam, scams, or self-promotion 🚫📢\n"
            "3️⃣ Use English only in discussions 🇬🇧🗣️\n"
            "4️⃣ No hate speech, racism, or discrimination ❌🧠\n"
            "5️⃣ Avoid sharing explicit or adult content 🔞🚫\n"
            "6️⃣ Do not post fake news or misleading info 📰⚠️\n"
            "7️⃣ Keep conversations on-topic 📌🗨️\n"
            "8️⃣ No unsolicited private messages to members 📵📩\n"
            "9️⃣ Report suspicious behavior to admins 🕵️‍♂️📣\n"
            "🔟 Admin decisions are final — follow instructions 👮✅",
            parse_mode="Markdown"
        )

    elif query.data == 'links':
        await query.message.reply_text(
            "🔗 Useful Links:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🌐 Telegram", url="https://telegram.org")],
                [InlineKeyboardButton("📺 Join Channel", url="https://t.me/cryptochainnetwork")],
                [InlineKeyboardButton("🪙 Crypto Portal", url="https://cryptoportal.byethost8.com")]
            ])
        )

    elif query.data == 'about':
        await query.message.reply_text(
            "🤖 This bot helps manage your group.\n"
            "It welcomes new members, filters spam, and shares useful info.\n"
            "Built by Gbenga 💻",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("👨‍💻 Developer", url="https://t.me/adeboye_99")],
                [InlineKeyboardButton("📢 Updates Channel", url="https://t.me/cryptochainnetwork")]
            ])
        )

    elif query.data == 'accept_rules':
        await query.edit_message_text("✅ Thank you! You may now participate in the group.")

# === WALLET ISSUE SUPPORT FLOW ===

async def wallet_issue_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🧾 Please enter your email address:")
    return ASK_EMAIL

async def ask_issue(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['email'] = update.message.text
    await update.message.reply_text("⚙️ Briefly describe the problem with your wallet or account:")
    return ASK_ISSUE

async def ask_q1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['issue'] = update.message.text
    await update.message.reply_text("❓ How long have you been facing this issue?")
    return ASK_Q1

async def ask_q2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['q1'] = update.message.text
    await update.message.reply_text("❓ Have you tried resolving it through your wallet provider?")
    return ASK_Q2

async def ask_q3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['q2'] = update.message.text
    await update.message.reply_text("❓ Which wallet or platform are you using?")
    return ASK_Q3

async def summary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['q3'] = update.message.text
    user_info = context.user_data

    summary_message = (
        f"✅ *Information Collected:*\n\n"
        f"📧 Email: {user_info.get('email')}\n"
        f"💬 Issue: {user_info.get('issue')}\n"
        f"🕓 Duration: {user_info.get('q1')}\n"
        f"🔧 Tried Fix: {user_info.get('q2')}\n"
        f"💼 Platform: {user_info.get('q3')}\n\n"
        f"Our support team will contact you soon. Thank you!"
    )

    await update.message.reply_text(summary_message, parse_mode="Markdown")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Operation cancelled.")
    return ConversationHandler.END

# === MAIN ===
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Command handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("rules", rules_command))
    app.add_handler(CommandHandler("links", links_command))
    app.add_handler(CommandHandler("about", about_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, filter_messages))
    app.add_handler(ChatMemberHandler(welcome, ChatMemberHandler.CHAT_MEMBER))

    # Wallet issue conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("wallet_issue", wallet_issue_command)],
        states={
            ASK_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_issue)],
            ASK_ISSUE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_q1)],
            ASK_Q1: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_q2)],
            ASK_Q2: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_q3)],
            ASK_Q3: [MessageHandler(filters.TEXT & ~filters.COMMAND, summary)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    app.add_handler(conv_handler)

    print("✅ Bot is running...")
    await app.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
