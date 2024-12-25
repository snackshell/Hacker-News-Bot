import asyncio
import schedule
import time
from datetime import datetime
import pytz
from typing import List
from telegram.constants import ParseMode
from hn_service import fetch_top_stories
from message_formatter import format_story_message

async def send_daily_update(app, destinations: List[str]):
    stories = await fetch_top_stories()
    current_date = datetime.now(pytz.timezone('Africa/Addis_Ababa')).strftime('%B %d, %Y')
    message, reply_markup = format_story_message(stories, current_date)
    
    for destination in destinations:
        try:
            if "@" in destination:
                parts = destination.split('@')
                if len(parts) > 1 and parts[-1].isdigit():
                    channel_id = destination.rsplit('@', 1)[0]
                    thread_id = int(parts[-1])
                    await app.bot.send_message(
                        chat_id=channel_id,
                        text=message,
                        parse_mode=ParseMode.HTML,
                        disable_web_page_preview=True,
                        reply_markup=reply_markup,
                        message_thread_id=thread_id
                    )
                    print(f"Successfully sent daily update to topic thread: {destination}")
                else:
                    await app.bot.send_message(
                        chat_id=destination,
                        text=message,
                        parse_mode=ParseMode.HTML,
                        disable_web_page_preview=True,
                        reply_markup=reply_markup
                    )
                    print(f"Successfully sent daily update to group: {destination}")
            else:
                await app.bot.send_message(
                    chat_id=destination,
                    text=message,
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True,
                    reply_markup=reply_markup
                )
                print(f"Successfully sent daily update to group: {destination}")
        except Exception as e:
            print(f"Failed to send daily update to {destination}: {e}")
            await app.bot.send_message(
                chat_id="@TopHackersNewsDaily",  # Fallback notification
                text=f"⚠️ Failed to send daily update to {destination}. Error: {e}"
            )


import os

def schedule_daily_updates(app):
    destinations_str = os.getenv('TELEGRAM_DESTINATIONS')
    destinations = [dest.strip() for dest in destinations_str.split(',')] if destinations_str else []

    async def run_daily_update():
        await send_daily_update(app, destinations)

    loop = asyncio.get_event_loop()
    schedule.every().day.at("08:00").do(lambda: asyncio.run_coroutine_threadsafe(run_daily_update(), loop))

    def run_scheduler():
        while True:
            schedule.run_pending()
            time.sleep(60)
    
    import threading
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
