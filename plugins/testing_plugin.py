"""Start message

pattern: `/start$`
"""

from telethon import client, events
from .global_functions import probability, log


# /start
# @events.register(events.NewMessage())
async def on_start(event):
    if event.is_private:    # If command was sent in private
        thing = event.message.media
        print(thing)
        # await log(event, "hello")
        await event.respond('boooop')
