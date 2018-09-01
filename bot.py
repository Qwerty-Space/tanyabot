import configparser
import logging
from random import random, randint
import re
from datetime import datetime
from os import path
from urllib.parse import urljoin

from telethon import TelegramClient, custom, events, sync

logging.basicConfig(level=logging.WARNING)


### VARIABLES ###
config = configparser.ConfigParser()
config.read_file(open("config.ini"))
token = config['DEFAULT']['TOKEN']
session_name = config['DEFAULT']['SESSION_NAME']
api_id = config['DEFAULT']['ID']
api_hash = config['DEFAULT']['HASH']
superadmin = int(config['DEFAULT']['superadmin'])
script_dir = path.dirname(path.realpath(__file__))  # Set the location of the script


### LOG IN TO TELEGRAM ##
print("Connecting...")
client = TelegramClient(path.join(script_dir, session_name), api_id, api_hash)


### FUNCTIONS ###
# Probability
def probability(percent):
    probability = random() < percent
    print(probability)


### "PLUGINS" ###
# /start
@client.on(events.NewMessage(pattern=r"(/start)$"))
async def on_start(event):
    sender = await event.get_sender()    # Get the sender
    if event.is_private:    # If command was sent in private
        print(f"[{event.date.strftime('%c')}] [{sender.id}] {sender.username}: {event.pattern_match.string}")
        await event.respond('This is a bot for silly replies')


# /ping
@client.on(events.NewMessage(pattern=r"(/ping)$"))
async def ping_pong(event):
    sender = await event.get_sender()
    if event.is_private:
        a = datetime.timestamp(datetime.now())
        message = await event.reply("**Pong!**")
        b = datetime.timestamp(datetime.now()) - a
        print(f"[{event.date.strftime('%c')}] [{sender.id}] {sender.username}: {event.pattern_match.string} [{b:.3f}]")
        await message.edit(f"**Pong!**\nTook `{b:.3f}` seconds")


# Hi, Hungry!
# Check if they say "I am" "I'm" or any variant of (+ at least 1, but at most 3 words)
@client.on(events.NewMessage(pattern=r"(?i)^(?:i'?m|i am) ((?:\S+ ?){1,3})$", outgoing=False, forwards=False))
async def i_am_dad(event):
    sender = await event.get_sender()
    print(f"[{event.date.strftime('%c')}] [{sender.id}] {sender.username}: {event.pattern_match.string}")
    if probability(0.2):    # Reply 20% of the time
        await event.reply("Hi " + event.pattern_match.group(1)) 


# MEIN FÜHRER!
@client.on(events.NewMessage(pattern=re.compile(r"(hitler|führer|fuhrer)", re.I).search, outgoing=False))
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


# Insult
@client.on(events.NewMessage(pattern=re.compile(r"(love|fuck|screw|damn?) (you|u) Tanya", re.I).search, outgoing=False, forwards=False))
async def insult(event):
    sender = await event.get_sender()
    print(f"[{event.date.strftime('%c')}] [{sender.id}] {sender.username}: {event.pattern_match.string}")
    await event.reply(event.pattern_match.group(1)+" you too!")    # "Love you too!"


# Hahahahahaha
@client.on(events.NewMessage(pattern=re.compile(r"(hah?\w+a)$", re.I).match, outgoing=False))
async def haha(event):
    sender = await event.get_sender()
    response_length = randint(2,5)
    response = event.pattern_match.group(1)*response_length    # Format the response (between 2 to 5 times the original length)
    print([datetime.now().strftime("%c")], [sender.id], sender.username, [response_length], event.pattern_match.string)
    if probability(0.2):
        await event.reply(response.capitalize())    # Capitalize the response


# Yes or no
@client.on(events.NewMessage(pattern=re.compile(r"(yes|y)(/| or )(no|n)\??$").search, forwards=False))    # Matches "y/n" "yes or no" "yes/no?" etc
async def yes_or_no(event):
    sender = await event.get_sender()
    print(f"[{event.date.strftime('%c')}] [{sender.id}] {sender.username}: {event.pattern_match.string}")
    if probability(0.5):
        await event.reply("Yes.")
    else:
        await event.reply("No.")


# Did you just assume their gender?!
@client.on(events.NewMessage(pattern=re.compile(r"\b(he|his|she|her)\b").search, forwards=False))
async def assume(event):
    sender = await event.get_sender()
    print(f"[{event.date.strftime('%c')}] [{sender.id}] {sender.username}: {event.pattern_match.string}")
    if probability(0.2):
        await event.reply("Did you just assume their gender?!")


# Subreddit
@client.on(events.NewMessage(pattern=re.compile(r"(?:\s|^)(/)?(r/)(\w+)\b").search))
async def link_subreddit(event):
    sender = await event.get_sender()
    subreddit_name = event.pattern_match.group(3)
    subreddit_link = urljoin("https://reddit.com/r/", subreddit_name)
    print(f"[{event.date.strftime('%c')}] [{sender.id}] {sender.username}: {event.pattern_match.string}")
    await event.reply(f"[/r/{subreddit_name}]({subreddit_link})", link_preview=".np" not in event.raw_text)


client.start(bot_token=token)

try:
    client.send_message(superadmin, "**Bot started at:**  "+datetime.now().strftime("`%c`"))
except ValueError:
    pass

print("Bot started at:  "+datetime.now().strftime("%c"))
client.run_until_disconnected()
