import aiohttp
import asyncio
from typing import List, Dict, Any

HN_API_BASE = 'https://hacker-news.firebaseio.com/v0'
MAX_RETRIES = 3
RETRY_DELAY = 1

async def fetch_with_retry(url: str, retries: int = MAX_RETRIES) -> Dict[str, Any]:
    async with aiohttp.ClientSession() as session:
        for attempt in range(retries):
            try:
                async with session.get(url) as response:
                    return await response.json()
            except Exception as e:
                if attempt == retries - 1:
                    raise e
                await asyncio.sleep(RETRY_DELAY)

async def fetch_top_stories() -> List[Dict[str, Any]]:
    # Fetch top stories IDs
    top_stories_ids = await fetch_with_retry(f"{HN_API_BASE}/topstories.json")
    top_10_ids = top_stories_ids[:10]
    
    # Fetch story details in parallel
    tasks = [
        fetch_with_retry(f"{HN_API_BASE}/item/{story_id}.json")
        for story_id in top_10_ids
    ]
    stories = await asyncio.gather(*tasks)
    
    return stories
