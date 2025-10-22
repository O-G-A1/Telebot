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

# full restored & fixed bot — async main (use with BOT_TOKEN env var on Railway)
import asyncio
import logging
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardRemove
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    ConversationHandler,
    ChatMemberHandler,
    filters
)
import os
import nest_asyncio

# allow nested event loop on some hosts (keep if you used it previously)
nest_asyncio.apply()

# --- logging ---
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- token check (will exit if missing) ---
BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    print("❌ BOT_TOKEN is missing. Set the BOT_TOKEN environment variable.")
    raise SystemExit(1)

# --- banned words (unchanged) ---
BANNED_WORDS = [
    'spam', 'scam', 'badword', 'fake', 'fraud', 'click here',
    'free money', 'nude', 'xxx', 'porn', 'sex', 'hate', 'racist',
    'terror', 'kill', 'bomb', 'attack', 'drugs', 'weapon', 'casino',
    'betting', 'gamble', 'credit card', 'make money fast', 'urgent',
    'viagra', 'escort', 'adult', 'explicit', 'nsfw', 'malware',
    'phishing', 'get rich quick'
]

# --- Conversation States (email → wallet → q1 → q2 → q3 → q4) ---
ASK_EMAIL, ASK_WALLET, ASK_Q1, ASK_Q2, ASK_Q3, ASK_Q4 = range(6)

# --- welcome handler (ChatMemberHandler) ---
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # ChatMemberHandler sends ChatMemberUpdated — new_chat_members is a pattern from earlier versions.
    # To keep compatibility with the previous code, we check for new_chat_member in the update.
    # If running PTB v20+, ChatMemberHandler delivers ChatMemberUpdated objects; here we attempt to send a simple welcome.
    try:
        for member in update.chat_member.new_chat_members:
            await update.effective_chat.send_message(
                f"👋 Welcome {member.full_name}! Please read the group rules with /rules."
            )
    except Exception:
        # Fallback: if structure is different, ignore safely
        logger.debug("welcome handler invoked but update.chat_member.new_chat_members not present.")

# --- filter messages for banned words ---
async def filter_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    text = update.message.text.lower()
    if any(word in text for word in BANNED_WORDS):
        try:
            await update.message.delete()
        except Exception:
            logger.debug("Could not delete message (missing permissions?).")
        await update.message.reply_text("⚠️ Message deleted: contains banned words.")

# --- start command (shows main menu with Report a Problem) ---
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🆘 Report a Problem", callback_data='support')],
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

# --- help command (also shows support) ---
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🆘 Report a Problem", callback_data='support')],
        [InlineKeyboardButton("🔗 Links", callback_data='links')],
        [InlineKeyboardButton("ℹ️ About", callback_data='about')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("📘 Choose a help option:", reply_markup=reply_markup)

# --- rules command ---
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

# --- links command ---
async def links_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🌐 Telegram", url="https://telegram.org")],
        [InlineKeyboardButton("📺 Join Channel", url="https://t.me/cryptochainnetwork")],
        [InlineKeyboardButton("🪙 Crypto Portal", url="https://cryptoportal.byethost8.com")]
    ]
    await update.message.reply_text("🔗 Useful Links:", reply_markup=InlineKeyboardMarkup(keyboard))

# --- about command ---
async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("👨‍💻 Developer", url="https://t.me/gbenga")],
        [InlineKeyboardButton("📢 Updates Channel", url="https://t.me/cryptochainnetwork")]
    ]
    await update.message.reply_text(
        "🤖 This bot helps manage your group.\nIt welcomes new members, filters spam, and provides support.\nBuilt by Gbenga 💻",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# --- callback button handler (handles support and menu buttons) ---
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
        return

    if query.data == 'links':
        await query.edit_message_text(
            "🔗 Useful Links:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🌐 Telegram", url="https://telegram.org")],
                [InlineKeyboardButton("📺 Join Channel", url="https://t.me/cryptochainnetwork")],
                [InlineKeyboardButton("🪙 Crypto Portal", url="https://cryptoportal.byethost8.com")]
            ])
        )
        return

    if query.data == 'about':
        await query.edit_message_text(
            "🤖 This bot helps manage your group.\nIt welcomes new members, filters spam, and provides support.\nBuilt by Gbenga 💻",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("👨‍💻 Developer", url="https://t.me/gbenga")],
                [InlineKeyboardButton("📢 Updates Channel", url="https://t.me/cryptochainnetwork")]
            ])
        )
        return

    if query.data == 'accept_rules':
        await query.edit_message_text("✅ Thank you! You may now participate in the group.")
        return

    if query.data == 'support':
        # enter support conversation via callback — start_support will be the entry point
        return await start_support(update, context)

# --- Support conversation flow (entry via callback or /support command) ---
async def start_support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # if called from CallbackQueryHandler, update.callback_query exists
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.message.reply_text(
            "🆘 Let's help you with your wallet or account issue.\nPlease enter your *email address* 📧:",
            parse_mode="Markdown"
        )
    else:
        # invoked as a command
        await update.message.reply_text("🆘 Let's help you with your wallet or account issue.\nPlease enter your *email address* 📧:", parse_mode="Markdown")
    return ASK_EMAIL

async def ask_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # store email and ask next question
    text = update.message.text.strip()
    context.user_data["email"] = text
    await update.message.reply_text(
        "💼 What *wallet or app* are you using? (e.g. Trust Wallet, MetaMask, Binance, etc.)",
        parse_mode="Markdown"
    )
    return ASK_WALLET

async def ask_q1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["wallet_name"] = update.message.text.strip()
    await update.message.reply_text(
        "❓ How long have you been experiencing this issue? (e.g. 2 hours, since yesterday, etc.)"
    )
    return ASK_Q1

async def ask_q2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["q1"] = update.message.text.strip()
    await update.message.reply_text(
        "🧩 Did you recently perform any transaction or update before the issue started?"
    )
    return ASK_Q2

async def ask_q3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["q2"] = update.message.text.strip()
    await update.message.reply_text(
        "📅 Have you tried accessing your wallet from another device?"
    )
    return ASK_Q3

async def ask_q4(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["q3"] = update.message.text.strip()
    await update.message.reply_text(
        "🔐 Have you backed up your recovery phrase or keys recently?"
    )
    return ASK_Q4

async def finish_support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["q4"] = update.message.text.strip()
    user = update.effective_user

    email = context.user_data.get("email")
    wallet = context.user_data.get("wallet_name")
    q1 = context.user_data.get("q1")
    q2 = context.user_data.get("q2")
    q3 = context.user_data.get("q3")
    q4 = context.user_data.get("q4")

    summary = (
        f"🆘 *Support Request Received!*\n\n"
        f"👤 *User:* {user.first_name} (@{user.username or 'N/A'})\n"
        f"📧 *Email:* {email}\n"
        f"💼 *Wallet/App:* {wallet}\n"
        f"❓ *Duration of issue:* {q1}\n"
        f"🧩 *Recent action before issue:* {q2}\n"
        f"📅 *Tried other device:* {q3}\n"
        f"🔐 *Backed up recovery keys:* {q4}"
    )

    # reply to user
    await update.message.reply_text("✅ Thank you! Our support team will contact you soon.")
    # send to admin (replace with your actual admin chat id)
    ADMIN_CHAT_ID = "YOUR_TELEGRAM_ID_HERE"
    try:
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=summary, parse_mode="Markdown")
    except Exception as e:
        logger.warning(f"Failed to send support summary to admin: {e}")

    return ConversationHandler.END

async def cancel_support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Support process cancelled.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

# --- fallback / cancel command ---
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Operation cancelled.")
    return ConversationHandler.END

# --- main async runner ---
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Register standard command handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("rules", rules_command))
    app.add_handler(CommandHandler("links", links_command))
    app.add_handler(CommandHandler("about", about_command))

    # CallbackQueryHandler for buttons (rules, links, about, support)
    app.add_handler(CallbackQueryHandler(button_handler))

    # Message filter for banned words
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, filter_messages))

    # ChatMember (welcome). Keep as in earlier working code — if your PTB version uses a different signature, adjust.
    try:
        app.add_handler(ChatMemberHandler(welcome, ChatMemberHandler.CHAT_MEMBER))
    except Exception:
        # Fallback: if ChatMemberHandler constant inaccessible on your version, just skip adding it
        logger.debug("ChatMemberHandler not added (version mismatch).")

    # Conversation handler for the support flow — entry via callback (support button) or direct command
    support_conv = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(start_support, pattern='^support$'),
            CommandHandler("support", start_support)
        ],
        states={
            ASK_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_wallet)],
            ASK_WALLET: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_q1)],
            ASK_Q1: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_q2)],
            ASK_Q2: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_q3)],
            ASK_Q3: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_q4)],
            ASK_Q4: [MessageHandler(filters.TEXT & ~filters.COMMAND, finish_support)],
        },
        fallbacks=[CommandHandler("cancel", cancel_support)],
        allow_reentry=True
    )
    app.add_handler(support_conv)

    logger.info("✅ Bot is running...")
    # run_polling is a coroutine in PTB v20; await it
    await app.run_polling()

if __name__ == "__main__":
    # Run the async main — this is the pattern that worked earlier
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped.")
