import asyncio
import schedule
import time
from datetime import datetime
import pytz
from telegram.constants import ParseMode
from hn_service import fetch_top_stories
from message_formatter import format_story_message

async def send_daily_update(app, chat_id: str):
    try:
        stories = await fetch_top_stories()
        current_date = datetime.now(pytz.timezone('Africa/Addis_Ababa')).strftime('%B %d, %Y')
        message, reply_markup = format_story_message(stories, current_date)
        
        await app.bot.send_message(
            chat_id=chat_id,
            text=message,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True,
            reply_markup=reply_markup
        )
    except Exception as e:
        print(f"Failed to send daily update: {e}")
        await app.bot.send_message(
            chat_id=chat_id,
            text="⚠️ Failed to send daily update. Please check the logs."
        )

def schedule_daily_updates(app, chat_id: str):
    def run_daily_update():
        asyncio.run(send_daily_update(app, chat_id))
    
    # Schedule for 8:00 AM EAT
    schedule.every().day.at("08:00").do(run_daily_update)
    
    def run_scheduler():
        while True:
            schedule.run_pending()
            time.sleep(60)
    
    import threading
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
