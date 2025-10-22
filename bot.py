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
# import logging
# nest_asyncio.apply()

# # --- Logging ---
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # --- Config ---
# BOT_TOKEN = os.environ.get("BOT_TOKEN")
# if not BOT_TOKEN:
#     logger.error("❌ BOT_TOKEN is missing. Set BOT_TOKEN environment variable.")
#     raise SystemExit(1)

# # Replace with your numeric Telegram user id (make sure you've started a DM with the bot)
# ADMIN_USER_ID = 7432554286

# # --- Conversation states ---
# ASK_EMAIL, ASK_PLATFORM, ASK_DESCRIPTION, ASK_EXTRA1, ASK_EXTRA2 = range(5)

# # --- Banned words (unchanged) ---
# BANNED_WORDS = [
#     'spam', 'scam', 'fake', 'fraud', 'nude', 'porn', 'sex', 'hate',
#     'terror', 'bomb', 'weapon', 'casino', 'betting', 'gamble', 'phishing'
# ]

# # --- Welcome / Goodbye handlers (use StatusUpdate handlers) ---
# async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     # update.message.new_chat_members is a list
#     if not update.message or not update.message.new_chat_members:
#         return
#     for member in update.message.new_chat_members:
#         try:
#             await update.message.reply_text(
#                 f"👋 Welcome {member.mention_html()}!\nPlease read the group rules with /rules.",
#                 parse_mode="HTML"
#             )
#         except Exception as e:
#             logger.warning(f"Failed to send welcome message: {e}")

# async def goodbye(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     if update.message and update.message.left_chat_member:
#         try:
#             await update.message.reply_text(
#                 f"👋 {update.message.left_chat_member.full_name} has left the group."
#             )
#         except Exception as e:
#             logger.warning(f"Failed to send goodbye message: {e}")

# # --- Basic command handlers ---
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

# async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     keyboard = [
#         [InlineKeyboardButton("📜 Rules", callback_data='rules')],
#         [InlineKeyboardButton("🔗 Links", callback_data='links')],
#         [InlineKeyboardButton("🚨 Report a Problem", callback_data='report_problem')]
#     ]
#     await update.message.reply_text("📘 Choose a help option:", reply_markup=InlineKeyboardMarkup(keyboard))

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
#     # If called from callback_query we should edit message or reply; handle both
#     if update.callback_query:
#         await update.callback_query.edit_message_text(rules_text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))
#     else:
#         await update.message.reply_text(rules_text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

# async def links_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     keyboard = [
#         [InlineKeyboardButton("📺 Join Channel", url="https://t.me/cryptochainnetwork")],
#         [InlineKeyboardButton("🌐 Telegram", url="https://telegram.org")]
#     ]
#     if update.callback_query:
#         await update.callback_query.edit_message_text("🔗 Useful Links:", reply_markup=InlineKeyboardMarkup(keyboard))
#     else:
#         await update.message.reply_text("🔗 Useful Links:", reply_markup=InlineKeyboardMarkup(keyboard))

# async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     keyboard = [
#         [InlineKeyboardButton("👨‍💻 Developer", url="https://t.me/gbenga")],
#         [InlineKeyboardButton("📢 Updates Channel", url="https://t.me/cryptochainnetwork")]
#     ]
#     text = "🤖 This bot helps manage your group.\nIt welcomes new members, filters spam, and shares info.\nBuilt by Gbenga 💻"
#     if update.callback_query:
#         await update.callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
#     else:
#         await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

# # --- Menu callback handler for non-conversation buttons ---
# async def menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     query = update.callback_query
#     await query.answer()
#     data = query.data

#     if data == "rules":
#         await rules_command(update, context)
#     elif data == "links":
#         await links_command(update, context)
#     elif data == "about":
#         await about_command(update, context)
#     elif data == "accept_rules":
#         await query.edit_message_text("✅ Thank you! You may now participate in the group.")
#     # note: 'report_problem' is handled by the ConversationHandler entry (see below)

# # --- Conversation (report) flow entry point (CallbackQueryHandler for report button) ---
# async def start_report_conv(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     # entry from callback query (button)
#     query = update.callback_query
#     await query.answer()
#     # Send initial prompt
#     await query.message.reply_text("📧 Please enter your email address:")
#     return ASK_EMAIL

# # --- Conversation states handlers ---
# async def ask_platform(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     # store email
#     context.user_data["email"] = update.message.text.strip()
#     await update.message.reply_text("💼 What wallet or platform are you having issues with?")
#     return ASK_PLATFORM

# async def ask_description(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     context.user_data["platform"] = update.message.text.strip()
#     await update.message.reply_text("📝 Please describe your issue briefly:")
#     return ASK_DESCRIPTION

# async def ask_extra1(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     context.user_data["description"] = update.message.text.strip()
#     await update.message.reply_text("❓ Additional info (if any)? If none, type 'None':")
#     return ASK_EXTRA1

# async def ask_extra2(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     # last answer
#     # depending on which state we used, we may need to shift storage
#     # Here we expect this to be ASK_EXTRA1 -> store into extra1, then prompt for extra2
#     if "extra1" not in context.user_data:
#         context.user_data["extra1"] = update.message.text.strip()
#         await update.message.reply_text("📌 Any screenshot or reference link? If none, type 'None':")
#         return ASK_EXTRA2
#     else:
#         context.user_data["extra2"] = update.message.text.strip()

#     # build final report (if extra2 present)
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

#     # reply to user
#     await update.message.reply_text("✅ Thank you! Our team will review your report soon.")

#     # send to admin (attempt, log on failure)
#     try:
#         await context.bot.send_message(chat_id=ADMIN_USER_ID, text=report, parse_mode="Markdown")
#         logger.info(f"Report sent to admin {ADMIN_USER_ID}")
#     except Exception as e:
#         logger.error(f"Failed to send report to admin {ADMIN_USER_ID}: {e}")
#         # fallback: print to stdout for Railway logs
#         print("REPORT (fallback):")
#         print(report)
#     finally:
#         # clear user_data for cleanliness
#         context.user_data.clear()

#     return ConversationHandler.END

# # alternate flow where we have ASK_EXTRA1 then ASK_EXTRA2 separately for clearer mapping
# async def ask_extra1_store(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     context.user_data["extra1"] = update.message.text.strip()
#     await update.message.reply_text("📌 Any screenshot or reference link? If none, type 'None':")
#     return ASK_EXTRA2

# async def ask_extra2_store_and_finish(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     context.user_data["extra2"] = update.message.text.strip()

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
#         logger.info("Report sent to admin.")
#     except Exception as e:
#         logger.error(f"Failed to send report to admin: {e}")
#         print(report)
#     context.user_data.clear()
#     return ConversationHandler.END

# # --- Cancel handler ---
# async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text("❌ Operation cancelled.")
#     context.user_data.clear()
#     return ConversationHandler.END

# # --- Message filter for banned words ---
# async def filter_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     if not update.message or not update.message.text:
#         return
#     text = update.message.text.lower()
#     if any(word in text for word in BANNED_WORDS):
#         try:
#             await update.message.delete()
#         except Exception:
#             logger.debug("Could not delete message (permissions?).")
#         await update.message.reply_text("⚠️ Message deleted: contains banned words.")

# # --- Main application runner ---
# async def main():
#     app = ApplicationBuilder().token(BOT_TOKEN).build()

#     # Conversation handler: entry via callback query when user clicks "report_problem"
#     conv = ConversationHandler(
#         entry_points=[CallbackQueryHandler(start_report_conv, pattern="^report_problem$")],
#         states={
#             ASK_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_platform)],
#             ASK_PLATFORM: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_description)],
#             ASK_DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_extra1_store)],
#             ASK_EXTRA1: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_extra2_store_and_finish)],
#             # ASK_EXTRA2 is terminal in this mapping
#         },
#         fallbacks=[CommandHandler("cancel", cancel)],
#         allow_reentry=True
#     )

#     # Add handlers - order matters a bit: conversation then menu callback
#     app.add_handler(conv)
#     app.add_handler(CallbackQueryHandler(menu_callback, pattern="^(rules|links|about|accept_rules)$"))
#     app.add_handler(CommandHandler("start", start_command))
#     app.add_handler(CommandHandler("help", help_command))
#     app.add_handler(CommandHandler("rules", rules_command))
#     app.add_handler(CommandHandler("links", links_command))
#     app.add_handler(CommandHandler("about", about_command))

#     # Status updates for new/left members
#     app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
#     app.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, goodbye))

#     # Filter & other messages
#     app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, filter_messages))

#     logger.info("Bot starting...")
#     await app.run_polling()

# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(main())
