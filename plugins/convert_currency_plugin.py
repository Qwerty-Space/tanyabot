from telethon import events
from currency_converter import CurrencyConverter
c = CurrencyConverter()


# Convert Currency
async def currency(event):
    sender = await event.get_sender()  # Get the sender

    fromval = event.pattern_match.group(1)
    if not fromval:
        fromval = 1
    fromcur = event.pattern_match.group(2).upper()
    tocur = event.pattern_match.group(3).upper()
    try:
        result = round(c.convert(fromval, fromcur, tocur), 2)
        print(f"[{event.date.strftime('%c')}] [{sender.id}] {sender.username}: {event.pattern_match.string}: {result}")
        await event.reply(f"**{fromval} {fromcur} is:**  `{result} {tocur}`")
    except ValueError:
        print(f"[{event.date.strftime('%c')}] [{sender.id}] {sender.username}:  {event.pattern_match.string}:  NOT AVAILABLE")
        link = "https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html"
        await event.reply(
            f"**Sorry, that currency is not supported yet.**\nFor a list of supported currencies [click here.](%s)"
            % (link),
            link_preview=False
        )

currency.event = events.NewMessage(pattern=r"^(\d{1,9}|\d{1,9}\.\d\d?)? ?([a-z]{3}) (?:to|in) (\D{3})$")
