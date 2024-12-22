from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.constants import ParseMode
from datetime import datetime
import pytz
import os
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
    await update.message.reply_text(
        welcome_message,
        message_thread_id=update.message.message_thread_id
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "🤖 Hacker News Bot Commands:\n\n"
        "/getnews: Show the latest top 10 Hacker News\n"
        "/help: Display this help message\n\n"
        "This bot fetches top tech news from Hacker News daily at 8:00 AM EAT."
    )
    await update.message.reply_text(
        help_text,
        parse_mode=ParseMode.HTML,
        message_thread_id=update.message.message_thread_id
    )

async def top_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        stories = await fetch_top_stories()
        current_date = datetime.now(pytz.timezone('Africa/Addis_Ababa')).strftime('%B %d, %Y')
        message, reply_markup = format_story_message(stories, current_date)
        
        await update.message.reply_text(
            message,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            message_thread_id=update.message.message_thread_id
        )
    except Exception as e:
        print(f"Error handling /getnews command: {e}")
        await update.message.reply_text(
            "⚠️ Failed to fetch top stories. Please try again later.",
            message_thread_id=update.message.message_thread_id
        )

async def send_to_topic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = int(os.getenv('TELEGRAM_CHAT_ID'))  # Load the group ID from .env
    topic_id = int(os.getenv('TELEGRAM_TOPIC_ID'))  # Load the topic ID from .env

    await context.bot.send_message(
      text="Hello! This message is sent to the topic!",
        message_thread_id=topic_id
    )
       chat_id=chat_id,
   
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Error occurred: {context.error}")
    if update and update.message:
        await update.message.reply_text(
            "An error occurred while processing your request.",
            message_thread_id=update.message.message_thread_id
        )

def main():
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    topic_id = os.getenv('TELEGRAM_TOPIC_ID')
    
    app = Application.builder().token(token).build()
    
    # Add command handlers
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('getnews', top_command))
    
    # Add error handler
    app.add_error_handler(error_handler)
    
    # Schedule daily updates
    schedule_daily_updates(app, chat_id, topic_id)
    
    # Start the bot
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
