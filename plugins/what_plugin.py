r"""When a user says "wot" the bot will reply with the previous message in BOLD CAPS.

Limits to once every 30 minutes.

pattern:  `(?i)^w[aou]t$`
"""

from telethon import events, sync
from .global_functions import log, cooldown

# Can't you hear?!
@events.register(events.NewMessage(pattern=r"(?i)^w[aou]t$"))
@cooldown(1800)
async def wut(event):
    if event.is_reply:
        replied_msg = await event.get_reply_message()
        msg_text = replied_msg.raw_text
    else:
        prev_id = (event.id)-1
        prev_msg = await event.client.get_messages(event.chat_id, ids=prev_id)
        msg_text = prev_msg.raw_text
    if msg_text:
        await event.reply(msg_text.upper())
        await log(event)
