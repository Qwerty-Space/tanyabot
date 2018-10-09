"""Converts celsius to fahrenheit and back.  Example:
"5°C in degrees f"
Accepts variations of "°C", for example "c", "degrees Celsius", or "degrees C".
Case insensitive.

patterns:
`(?i)^(\d{1,9}|-\d{1,9})( ?° ?| degrees)? ?c(elsius)? (to|in) (°|degrees)?f(ahrenheit)?$`
`(?i)^(\d{1,9}|-\d{1,9})( ?° ?| degrees)? ?f(ahrenheit)? (to|in) (°|degrees)?c(elsius)?$`
"""

import re
from telethon import events, sync
from .global_functions import probability


#Convert Celsius to Fahrenheit
@events.register(events.NewMessage(pattern=re.compile(r"^(\d{1,9}|-\d{1,9})( ?° ?| degrees)? ?c(elsius)? (to|in) (°|degrees)?f(ahrenheit)?$", re.I).search))
async def c_to_f(event):
    sender = await event.get_sender()
    c = int(event.pattern_match.group(1))
    sum = (c * 1.8) + 32
    print(f"[{event.date.strftime('%c')}] [{sender.id}] {sender.username}: {event.pattern_match.string}: {sum}")
    await event.reply(f"**{c} °C is:**  `{sum} °F`")


#Convert Fahrenheit to Celsius
@events.register(events.NewMessage(pattern=re.compile(r"^(\d{1,9}|-\d{1,9})( ?° ?| degrees)? ?f(ahrenheit)? (to|in) (°|degrees)?c(elsius)?$", re.I).search))
async def f_to_c(event):
    sender = await event.get_sender()
    f = int(event.pattern_match.group(1))
    sum = (f - 32) * 0.55555555555
    print(f"[{event.date.strftime('%c')}] [{sender.id}] {sender.username}: {event.pattern_match.string}: {sum}")
    await event.reply(f"**{f} °F is:**  `{sum} °C`")
