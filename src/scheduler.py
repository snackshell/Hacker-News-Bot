import asyncio
import schedule
import time
from datetime import datetime
import pytz
from telegram.constants import ParseMode
from hn_service import fetch_top_stories
from message_formatter import format_story_message

async def send_daily_update(app, chat_id: str, topic_id: str = None):
    try:
        stories = await fetch_top_stories()
        current_date = datetime.now(pytz.timezone('Africa/Addis_Ababa')).strftime('%B %d, %Y')
        message, reply_markup = format_story_message(stories, current_date)
        
        await app.bot.send_message(
            chat_id=chat_id,
            message_thread_id=int(topic_id) if topic_id else None,
            text=message,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True,
            reply_markup=reply_markup
        )
    except Exception as e:
        print(f"Failed to send daily update: {e}")
        error_message = (
            f"⚠️ Failed to send daily update. Error: {str(e)}\n"
            "Please check the logs for more details."
        )
        await app.bot.send_message(
            chat_id=chat_id,
            message_thread_id=int(topic_id) if topic_id else None,
            text=error_message
        )

def schedule_daily_updates(app, chat_id: str, topic_id: str = None):
    def run_daily_update():
        try:
            asyncio.run(send_daily_update(app, chat_id, topic_id))
        except Exception as e:
            print(f"Scheduler error: {e}")
    
    # Schedule for 8:00 AM EAT
    schedule.every().day.at("12:50").do(run_daily_update)
    
    def run_scheduler():
        while True:
            try:
                schedule.run_pending()
                time.sleep(60)
            except Exception as e:
                print(f"Scheduler thread error: {e}")
                time.sleep(60)  # Wait before retrying
    
    import threading
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
