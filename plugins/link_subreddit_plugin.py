import re
from urllib.parse import urljoin
from telethon import events, sync
from global_functions import probability
from telethon.tl.types import MessageEntityTextUrl, MessageEntityUrl


# Subreddit
async def link_subreddit(event):
    """Matches `r/subreddit` and `/r/subreddit`, and will return the subreddit as a link (ignores messages with links).
**Arguments (positional):**
    • `.np`: - No preview
    • `.f`: - Force match"""
    sender = await event.get_sender()
    prefix = event.pattern_match.group(1)
    subreddit_name = event.pattern_match.group(2)
    suffix = event.pattern_match.group(3)
    if not suffix:
        suffix = ""
    subreddit_link = urljoin("https://reddit.com/", f"{prefix}/{subreddit_name}{suffix}")
    log = f"[{event.date.strftime('%c')}] [{sender.id}] {sender.username}: {event.pattern_match.string}"

    async def subreddit_reply():
        await event.reply(f"[/{prefix}/{subreddit_name}{suffix}]({subreddit_link})", link_preview=".np" not in event.raw_text)

    if not any(isinstance(x, (MessageEntityUrl, MessageEntityTextUrl)) for x in event.entities or []):
        print(log)
        await subreddit_reply()
    elif re.search(r".(np)?f", event.raw_text):
        print(log)
        await subreddit_reply()

link_subreddit.event = events.NewMessage(pattern=re.compile(
                r"(?:\s|^)/?(r|u)/(\w+)(/(?:top|best|new|hot|rising|gilded|controversial|wiki(?:/\S+)?))?\b"
                ).search)
