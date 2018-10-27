"""The bot will reply with the time it took to respond to your command.
Works in private only

pattern: `/ping$`
"""

from datetime import datetime
from telethon import events
from .global_functions import log

# /ping
@events.register(events.NewMessage(pattern=r"/ping$"))
async def ping_pong(event):
    if event.is_private:
        a = datetime.timestamp(datetime.now())
        message = await event.reply("**Pong!**")
        b = datetime.timestamp(datetime.now()) - a
        await log(event, f"{b:.3f}")
        await message.edit(f"**Pong!**\nTook `{b:.3f}` seconds")
