import os 
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.constants import ParseMode
from datetime import datetime
import pytz
from dotenv import load_dotenv

from hn_service import fetch_top_stories
from message_formatter import format_story_message
from scheduler import schedule_daily_updates

load_dotenv()

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = (
        "Yo, this is HN bot for @dagmawibabichat 📰\n\n"
        "I will send ya the top Hacker News stories every day at 8:00 AM EAT.\n\n"
        "Commands:\n"
        "/getnews - Get top stories now\n"
        "/help - Show help message"
    )
    await update.message.reply_text(welcome_message)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "🤖 Hacker News Bot Commands:\n\n"
        "/getnews: Show the latest top 10 Hacker News\n"
        "/help: Display this help message\n\n"
        "This bot fetches top tech news from Hacker News daily at 8:00 AM EAT."
    )
    await update.message.reply_text(help_text, parse_mode=ParseMode.HTML)

async def top_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        stories = await fetch_top_stories()
        current_date = datetime.now(pytz.timezone('Africa/Addis_Ababa')).strftime('%B %d, %Y')
        message, reply_markup = format_story_message(stories, current_date)
        
        # Send to the originating chat
        await update.message.reply_text(
            message,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True,
            reply_markup=reply_markup
        )
        
    except Exception as e:
        print(f"Error handling /getnews command: {e}")
        await update.message.reply_text(
            "⚠️ Failed to fetch top stories. Please try again later."
        )

def main():
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    app = Application.builder().token(token).build()
    
    # Add command handlers
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('getnews', top_command))  
    
    
    # Schedule daily updates
    schedule_daily_updates(app)
    
    # Start the bot
    app.run_polling()

if __name__ == "__main__":
    main()
