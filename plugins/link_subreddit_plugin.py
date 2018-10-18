r"""When a user mentions a subreddit, the bot will respond with a link to that page on the subreddit.

For example sending "/r/aww/top" will provide a link to the top or /r/aww

Adding `.np` anywhere in the message will remove the link preview.

pattern:  `(?i)(?:[^/\w]|^|\s)/?(r/\w+)(/(?:top|best|new|hot|rising|gilded|controversial|wiki(?:/\S+)?))?\b`
"""

import re
from urllib.parse import urljoin
from telethon import events, sync
from .global_functions import log
from telethon.tl.types import MessageEntityTextUrl, MessageEntityUrl


# Subreddit
@events.register(events.NewMessage(pattern=re.compile(
                    r"(?i)(?:[^/\w]|^|\s)/?(r/\w+)(/(?:top|best|new|hot|rising|gilded|controversial|wiki(?:/\S+)?))?\b"
                ).search))
async def link_subreddit(event):
    subreddit = event.pattern_match.group(1)
    suffix = event.pattern_match.group(2)
    if not suffix:
        suffix = ""
    subreddit_link = urljoin("https://reddit.com/", f"{subreddit}{suffix}")
    await log(event, ".np" not in event.raw_text)
    await event.reply(f"[/{subreddit}{suffix}]({subreddit_link})", link_preview=".np" not in event.raw_text)

