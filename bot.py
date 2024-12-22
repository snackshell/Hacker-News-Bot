import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler
import requests
from datetime import datetime
from dateutil import tz

# Replace with your Bot Token
BOT_TOKEN = "YOUR_BOT_API_TOKEN"

# Hacker News API endpoints
HN_TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
HN_ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

# Configure logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# Function to fetch and send Hacker News
async def send_hn_news(update: Update, context):
    chat_id = update.effective_chat.id
    top_stories = requests.get(HN_TOP_STORIES_URL).json()[:5]  # Get top 5 stories

    for story_id in top_stories:
        story = requests.get(HN_ITEM_URL.format(story_id)).json()
        title = story.get("title", "No Title")
        url = story.get("url", "No URL")
        comments_url = f"https://news.ycombinator.com/item?id={story_id}"  # Comments link

        # Create inline buttons
        keyboard = [
            [
                InlineKeyboardButton("🔗 Details", url=url),
                InlineKeyboardButton("💬 Comments", url=comments_url),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Send the message with buttons
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"📰 **{title}**",
            parse_mode="Markdown",
            reply_markup=reply_markup,
        )

# Function to send daily news at a specific time
async def daily_task(application):
    eth_timezone = tz.gettz("Africa/Addis_Ababa")  # Ethiopian timezone
    current_time = datetime.now(eth_timezone).time()

    if current_time.hour == 8:  # 8 AM Ethiopian time
        chat_id = "YOUR_GROUP_CHAT_ID"  # Replace with your group chat ID
        top_stories = requests.get(HN_TOP_STORIES_URL).json()[:5]
        for story_id in top_stories:
            story = requests.get(HN_ITEM_URL.format(story_id)).json()
            title = story.get("title", "No Title")
            url = story.get("url", "No URL")
            comments_url = f"https://news.ycombinator.com/item?id={story_id}"  # Comments link

            # Create inline buttons
            keyboard = [
                [
                    InlineKeyboardButton("🔗 Details", url=url),
                    InlineKeyboardButton("💬 Comments", url=comments_url),
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            # Send the message with buttons
            await application.bot.send_message(
                chat_id=chat_id,
                text=f"📰 **{title}**",
                parse_mode="Markdown",
                reply_markup=reply_markup,
            )

# Main function
def main():
    # Create the bot application
    application = Application.builder().token(BOT_TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("getnews", send_hn_news))

    # Schedule daily task
    application.job_queue.run_repeating(daily_task, interval=3600, first=0)  # Check every hour

    # Start the bot
    application.run_polling()

# Run the bot
if __name__ == "__main__":
    main()
