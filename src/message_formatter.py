from typing import List, Dict, Any
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def format_story_message(stories: List[Dict[str, Any]], current_date: str) -> str:
    header = f"🔥 <b>Top Hacker News - {current_date}</b>\n\n"
    
    story_list = []
    for index, story in enumerate(stories, 1):
        title = story['title']
        url = story.get('url') or f"https://news.ycombinator.com/item?id={story['id']}"
        score = story.get('score', 0)
        comments = story.get('descendants', 0)
        
        story_text = (
            f"{index}. <a href='{url}'>{title}</a>\n"
            f"📊 {score} points | 💬 {comments} comments\n"
        )
        story_list.append(story_text)
    
    stories_text = "\n".join(story_list)

    keyboard = [[InlineKeyboardButton("Visit Hacker News", url='https://news.ycombinator.com')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    return f"{header}{stories_text}", reply_markup
