# Convert weights to other common weights, the numbers are the given weight in grams

from telethon import events, sync
from .global_functions import log, cooldown


units = {
    "g": 1,
    "kg": 1000,
    "tonne": 1000000,
    "lbs": 453.59237,
    "oz": 28.349523125,
    "st": 6350.29318,
    "stone": 6350.29318,
    "ton": 1016046.9088
}


@events.register(events.NewMessage(pattern=r"(?i)^(\d+(?:(?:\.|,)\d+)?)? ?(k?g|ton(?:ne)|lbs|oz|st(?:one)) (?:to|in) (k?g|ton(?:ne)|lbs|oz|st(?:one))$"))
async def weight(event):
    value = float(event.pattern_match.group(1))

    if not value:
        value = 1
        
    unitfrom = event.pattern_match.group(2).lower()
    unitto = event.pattern_match.group(3).lower()

    result = round(value*units[unitfrom]/units[unitto], 3)
    await log(event, result)
    await event.reply(f"**{value} {unitfrom} is:**  `{result} {unitto}`")


@events.register(events.NewMessage(pattern=r"/weights(@\w+)?$"))
@cooldown(60)
async def list_weights(event):
    usr_group = event.pattern_match.group(1)
    username = (await event.client.get_me()).username
    if usr_group and username not in usr_group:
        return

    text = f"**List of supported weights:**\n{', '.join(sorted(units.keys()))}"
    await event.reply(text)
    await log(event)
