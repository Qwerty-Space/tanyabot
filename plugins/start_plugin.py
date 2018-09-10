from telethon import events, sync
from global_functions import probability

# /start
async def on_start(event):
    sender = await event.get_sender()    # Get the sender
    if event.is_private:    # If command was sent in private
        print(f"[{event.date.strftime('%c')}] [{sender.id}] {sender.username}: {event.pattern_match.string}")
        await event.respond('This is a bot for silly replies')

on_start.event = events.NewMessage(pattern=r"(/start)$")
