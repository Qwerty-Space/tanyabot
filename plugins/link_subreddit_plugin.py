r"""
When a user mentions a subreddit, the bot will respond with a link to that page on the subreddit.

For example sending "/r/aww/top" will provide a link to the top or /r/aww

pattern:  `(?i)(?:[^/\w]|^|\s)/?(r/\w+)(/(?:top|best|new|hot|rising|gilded|controversial|wiki(?:/\S+)?))?\b`
"""

import re
from urllib.parse import urljoin
from telethon import events, sync
from .global_functions import probability
from telethon.tl.types import MessageEntityTextUrl, MessageEntityUrl


# Subreddit
@events.register(events.NewMessage(pattern=re.compile(
                    r"(?i)(?:[^/\w]|^|\s)/?(r/\w+)(/(?:top|best|new|hot|rising|gilded|controversial|wiki(?:/\S+)?))?\b"
                ).search))
async def link_subreddit(event):
    """Matches `r/subreddit` and `/r/subreddit`, and will return the subreddit as a link.
**Arguments (positional):**
    • `.np`: - No preview
    """
    sender = await event.get_sender()
    subreddit = event.pattern_match.group(1)
    suffix = event.pattern_match.group(2)
    if not suffix:
        suffix = ""
    subreddit_link = urljoin("https://reddit.com/", f"{subreddit}{suffix}")
   
    print(f"[{event.date.strftime('%c')}] [{sender.id}] {sender.username}: {event.pattern_match.string}")
    await event.reply(f"[/{subreddit}{suffix}]({subreddit_link})", link_preview=".np" not in event.raw_text)

