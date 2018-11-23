r"""When a user mentions a subreddit, the bot will respond with a link to that page on the subreddit.

For example sending `/r/aww/top` will provide a link to the top of /r/aww

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
                ).findall))
async def link_subreddit(event):
    reply_msg = ""
    for s in event.pattern_match:
        subreddit = "".join(s)
        subreddit_link = urljoin("https://reddit.com/", subreddit)
        reply_msg += f"• [/{subreddit}]({subreddit_link})\n"
    link_bool = ".np" not in event.raw_text and len(event.pattern_match) < 2
    await log(event, ".np" not in event.raw_text)
    await event.reply(reply_msg, link_preview=link_bool)
