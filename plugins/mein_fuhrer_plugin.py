import re
from random import randint
from telethon import events, sync
from global_functions import probability


# MEIN FÜHRER!
async def mein_fuhrer(event):
    sender = await event.get_sender()
    response_id = randint(0,2) # Roll for the response
    print(f"[{event.date.strftime('%c')}] [{sender.id}] {sender.username}[{response_id}]: {event.pattern_match.string}")
    if response_id == 0:
        await event.reply("Heil Hitler!")
    elif response_id == 1:
        await event.reply("Sieg Heil!")
    elif response_id == 2:
        await event.reply(file = "CAADAgADWgADraG3CP76-OQcP7msAg")    # Send a sticker

mein_fuhrer.event =  events.NewMessage(pattern=re.compile(r"(hitler|führer|fuhrer)", re.I).search, outgoing=False)
