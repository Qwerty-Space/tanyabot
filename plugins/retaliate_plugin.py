import re
from telethon import events, sync
from global_functions import probability


# Insult
async def insult(event):
    sender = await event.get_sender()
    print(f"[{event.date.strftime('%c')}] [{sender.id}] {sender.username}: {event.pattern_match.string}")
    await event.reply(event.pattern_match.group(1)+" you too!")    # "Love you too!"

insult.event = events.NewMessage(pattern=re.compile(r"(love|fuck|screw|damn?) (you|u) Tanya", re.I).search, outgoing=False, forwards=False)
