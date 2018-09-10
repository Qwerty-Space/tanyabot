from telethon import events
from currency_converter import CurrencyConverter

c = CurrencyConverter()


# Convert Currency
async def currency(event):
    sender = await event.get_sender()  # Get the sender
    result = c.convert(event.pattern_match.group(1), event.pattern_match.group(2), event.pattern_match.group(3))
    print(f"[{event.date.strftime('%c')}] [{sender.id}] {sender.username}: {event.pattern_match.string}: {result}")
    await event.reply(
        f"**{event.pattern_match.group(1)} {event.pattern_match.group(2)} is:**  `{result} {event.pattern_match.group(3)}`")

currency.event = events.NewMessage(pattern=r"(^\d{1,9}|^\d{1,9}\.\d\d?) (\D{3}) to (\D{3})$")
