import re
from telethon import events, sync
from probability_function import probability


# Yes or no
async def yes_or_no(event):
    sender = await event.get_sender()
    print(f"[{event.date.strftime('%c')}] [{sender.id}] {sender.username}: {event.pattern_match.string}")
    if probability(0.5):
        await event.reply("Yes.")
    else:
        await event.reply("No.")

yes_or_no.event = events.NewMessage(pattern=re.compile(r"(yes|y)(/| or )(no|n)\??$").search, forwards=False)    # Matches "y/n" "yes or no" "yes/no?" etc
