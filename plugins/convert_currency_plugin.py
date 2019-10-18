r"""Converts two different currencies using the [European Central Bank's exchange rates](https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html).

Example: "GBP to/in USD" (case insensitive).
You can also specify an amount of said currency:
"5 GBP to USD".

List currencies using `/currencies`

patterns:  
`(?i)^(\d{1,9}|\d{1,9}\.\d\d?)? ?([a-z]{3}) (?:to|in) ([a-z]{3})$`

`/currencies(@bots_username)?$`
"""

from telethon import events
from currency_converter import CurrencyConverter
from .global_functions import log, cooldown

c = CurrencyConverter()
link = "https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html"


# Convert Currency
@events.register(events.NewMessage(pattern=r"(?i)^(\d{1,9}|\d{1,9}\.\d\d?)? ?([a-z]{3}) (?:to|in) ([a-z]{3})$"))
async def currency(event):
    fromval = event.pattern_match.group(1)

    if not fromval:
        fromval = 1
        
    fromcur = event.pattern_match.group(2).upper()
    tocur = event.pattern_match.group(3).upper()

    if fromcur.upper() not in c.currencies:
        return
    if tocur.upper() not in c.currencies:
        return

    result = round(c.convert(fromval, fromcur, tocur), 2)
    await log(event, result)
    await event.reply(f"**{fromval} {fromcur} is:**  `{result} {tocur}`")


@events.register(events.NewMessage(pattern=r"/currencies(@\w+)?$"))
@cooldown(60)
async def list_currencies(event):
    usr_group = event.pattern_match.group(1)
    username = (await event.client.get_me()).username
    if usr_group and username not in usr_group:
        return

    text = f"**List of supported currencies:**\n{', '.join(sorted(c.currencies))}\n\nFor a detailed list of supported currencies [click here.]({link})"
    await event.reply(text, link_preview=False)
    await log(event)
