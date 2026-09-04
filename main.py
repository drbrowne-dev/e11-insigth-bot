import os
import threading
from flask import Flask
from waitress import serve
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# --- 1. Flask Web Server Setup (For Render Hosting) ---
web_app = Flask(__name__)

@web_app.route('/')
def health_check():
    return "E11 Resource Bot is Active!", 200

def start_flask_server():
    port = int(os.environ.get("PORT", 8080))
    serve(web_app, host="0.0.0.0", port=port)

# --- 2. Environment Variables & Safety Checks ---
# Reads RESOURCE_BOT_TOKEN first; falls back to BOT_TOKEN if not found
TOKEN = os.getenv("RESOURCE_BOT_TOKEN") or os.getenv("BOT_TOKEN")

if not TOKEN:
    print("❌ FATAL: Bot token is completely missing from environment variables!")
    exit(1)

# --- 3. UI Keyboards & Navigation ---
def main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("📊 Indicators & Source Code", callback_data="menu_indicators")],
        [InlineKeyboardButton("🎓 Video Courses", callback_data="menu_courses")],
        [InlineKeyboardButton("📈 Trading Strategies", callback_data="menu_strategies")],
        [InlineKeyboardButton("📢 Official Channel", url="https://t.me/e11lab_TradingDesk_MarketInsight")]
    ]
    return InlineKeyboardMarkup(keyboard)

# --- 4. Bot Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        f"👋 **Welcome {update.effective_user.first_name} to E11 Lab Resources!**\n\n"
        "Explore our official trading tools, courses, and strategies using the buttons below:"
    )
    await update.message.reply_text(welcome_text, reply_markup=main_menu_keyboard(), parse_mode="Markdown")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # --- INDICATORS MENU ---
    if query.data == "menu_indicators":
        text = (
            "📊 **E11 Lab Indicators**\n\n"
            "• **Free Indicator:** [Download/Access Source Code](https://tradingview.com)\n"
            "• **Pro Suite (Paid):** Full access to institutional order-flow tools.\n"
            "  *Price:* $29/month or $199 Lifetime\n\n"
            "Contact support in our main bot to unlock Pro access!"
        )
        keyboard = [
            [InlineKeyboardButton("📥 Get Free Indicator", url="https://tradingview.com")],
            [InlineKeyboardButton("⬅️ Back to Main Menu", callback_data="main_menu")]
        ]
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown", disable_web_page_preview=True)

    # --- COURSES MENU ---
    elif query.data == "menu_courses":
        text = (
            "🎓 **E11 Trading Academy**\n\n"
            "Watch our step-by-step video courses to master market structure and risk management:"
        )
        keyboard = [
            [InlineKeyboardButton("🎬 Module 1: Market Structure (Free)", url="https://youtube.com")],
            [InlineKeyboardButton("🎬 Module 2: Risk & Execution", url="https://youtube.com")],
            [InlineKeyboardButton("⬅️ Back to Main Menu", callback_data="main_menu")]
        ]
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown", disable_web_page_preview=True)

    # --- STRATEGIES MENU ---
    elif query.data == "menu_strategies":
        text = (
            "📈 **Core Trading Strategies**\n\n"
            "1. **Liquidity Sweep & Mitigation:** Trade institutional key levels.\n"
            "2. **Session Breakout Strategy:** High-probability London/NY open plays.\n\n"
            "Click below to view the detailed strategy guides:"
        )
        keyboard = [
            [InlineKeyboardButton("📄 Read Liquidity Guide", url="https://t.me/E11LabCommunity")],
            [InlineKeyboardButton("⬅️ Back to Main Menu", callback_data="main_menu")]
        ]
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown", disable_web_page_preview=True)

    # --- BACK TO MAIN MENU ---
    elif query.data == "main_menu":
        text = "Select a resource category below:"
        await query.message.edit_text(text, reply_markup=main_menu_keyboard(), parse_mode="Markdown")

# --- 5. Application Launch ---
if __name__ == "__main__":
    # Start Web Server Thread for Render Keep-Alive
    threading.Thread(target=start_flask_server, daemon=True).start()

    # Build Telegram Bot
    print("🚀 E11 Resource Bot initializing...")
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    # Run Polling Loop
    app.run_polling(drop_pending_updates=True)
