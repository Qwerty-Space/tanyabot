from collections import defaultdict
from random import random
import logging
import asyncio
import time


# Probability
def probability(percent):
    outcome = random() < percent
    return outcome

# Logging
async def log(event, info=""):
    sender = await event.get_sender()
    try: 
        message = event.pattern_match.string
    except AttributeError:
        message = ""
    logging.info(
        f"""[{event.date.strftime('%c')}]:
    [{sender.id}]@[{event.chat.id}] {sender.first_name}@{sender.username}: {message}
    {info}""".rstrip())

# Cooldown
def cooldown(timeout):
    def wrapper(function):
        last_called = defaultdict(int)

        async def wrapped(event, *args, **kwargs):
            current_time = time.time()
            if current_time - last_called[event.chat_id] < timeout:
                time_left = round(timeout - (current_time - last_called[event.chat_id]), 1)
                await log(event, f"Cooldown: {time_left}s")
                return
            last_called[event.chat_id] = current_time
            return await function(event, *args, **kwargs)
        return wrapped
    return wrapper