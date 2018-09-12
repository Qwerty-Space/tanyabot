import re
from telethon import events, sync
from global_functions import probability


# No, this is Patrick!
async def this_is_patrick(event):
    sender = await event.get_sender()
    print(f"[{event.date.strftime('%c')}] [{sender.id}] {sender.username}: {event.pattern_match.string}")
    if probability(0.2):
        await event.reply("No, this is Patrick.")

this_is_patrick.event = events.NewMessage(pattern=re.compile(r"^is this ((?:\S+ ?){1,4})\??$", re.I).search)
