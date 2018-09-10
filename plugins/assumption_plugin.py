import re
from telethon import events, sync
from global_functions import probability


# Did you just assume their gender?!
async def assume(event):
    sender = await event.get_sender()
    print(f"[{event.date.strftime('%c')}] [{sender.id}] {sender.username}: {event.pattern_match.string}")
    if probability(0.2):
        await event.reply("Did you just assume their gender?!")

assume.event = events.NewMessage(pattern=re.compile(r"\b(he|his|she|her)\b").search, forwards=False)
