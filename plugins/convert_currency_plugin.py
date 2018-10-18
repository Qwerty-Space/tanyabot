"""Converts two different currencies using the [European Central Bank's exchange rates](https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html).

Example: "GBP to/in USD" (case insensitive).
You can also specify an amount of said currency:
"5 GBP to USD".

pattern:  `(?i)^(\d{1,9}|\d{1,9}\.\d\d?)? ?([a-z]{3}) (?:to|in) ([a-z]{3})$`
"""

from telethon import events
from currency_converter import CurrencyConverter
from .global_functions import log
c = CurrencyConverter()


# Convert Currency
@events.register(events.NewMessage(pattern=r"(?i)^(\d{1,9}|\d{1,9}\.\d\d?)? ?([a-z]{3}) (?:to|in) ([a-z]{3})$"))
async def currency(event):
    fromval = event.pattern_match.group(1)
    if not fromval:
        fromval = 1
    fromcur = event.pattern_match.group(2).upper()
    tocur = event.pattern_match.group(3).upper()
    try:
        result = round(c.convert(fromval, fromcur, tocur), 2)
        await log(event, result)
        await event.reply(f"**{fromval} {fromcur} is:**  `{result} {tocur}`")
    except ValueError:
        await log(event, "CURRENCY NOT AVAILABLE")
        link = "https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html"
        await event.reply(
            f"**Sorry, that currency is not supported yet.**\nFor a list of supported currencies [click here.](%s)"
            % (link),
            link_preview=False
        )
