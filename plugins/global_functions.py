from random import random
import logging

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
    {info}""")

