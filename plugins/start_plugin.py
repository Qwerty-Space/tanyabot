"""
Start message

pattern: `/start$`
"""

from telethon import client, events, sync
from .global_functions import probability


# /start
@events.register(events.NewMessage(pattern=r"/start$"))
async def on_start(event):
    sender = await event.get_sender()    # Get the sender
    if event.is_private:    # If command was sent in private
        print(f"[{event.date.strftime('%c')}] [{sender.id}] {sender.username}: {event.pattern_match.string}")
        await event.respond('This is a bot for silly replies.  See /help for a list of commands.')
