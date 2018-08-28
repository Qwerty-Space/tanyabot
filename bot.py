import configparser
import logging
import re
from datetime import datetime
from os import path
import random
randint = random.randint

from telethon import TelegramClient, custom, events, sync

logging.basicConfig(level=logging.WARNING)


### VARIABLES ###
config = configparser.ConfigParser()
config.read_file(open("config.ini"))
token = config['DEFAULT']['TOKEN']
session_name = config['DEFAULT']['SESSION_NAME']
api_id = config['DEFAULT']['ID']
api_hash = config['DEFAULT']['HASH']
script_dir = path.dirname(path.realpath(__file__))  # Set the location of the script
currentTime = datetime.now()


### LOG IN TO TELEGRAM ##
print("Connecting...")

client = TelegramClient(path.join(script_dir, session_name), api_id, api_hash)


### FUNCTIONS ###
# Probability
def probability(percent):
    probability = random.random() <= percent
    print(probability)
    return probability


### "PLUGINS" ###
# /start
@client.on(events.NewMessage(pattern="(/start)$"))
async def on_start(event):
    sender = await event.get_sender()    # Get the sender
    if event.is_private:    # If command was sent in private
        print([currentTime.strftime("%c")], [sender.id], sender.username, event.pattern_match.string)
        await event.respond('This is a bot for silly replies')


# Hi, Hungry!
# Check if they say "I am" "I'm" or any variant of (+ at least 1, but at most 3 words)
@client.on(events.NewMessage(pattern="(?i)^(?:i'?m|i am) ((?:\S+ ?){1,3})$", outgoing=False, forwards=False))
async def i_am_dad(event):
    sender = await event.get_sender()
    print([currentTime.strftime("%c")], [sender.id], sender.username, event.pattern_match.string)
    if probability(0.2):    # Reply 20% of the time
        await event.reply("Hi " + event.pattern_match.group(1)) 


# MEIN FÜHRER!
@client.on(events.NewMessage(pattern=re.compile("(hitler|führer|fuhrer)", re.I).search, outgoing=False))
async def mein_fuhrer(event):
    sender = await event.get_sender()
    response_id = randint(0,2) # Roll for the response
    print([currentTime.strftime("%c")], [sender.id], sender.username, [response_id], event.pattern_match.string)
    if response_id == 0:
        await event.reply("Heil Hitler!")
    elif response_id == 1:
        await event.reply("Sieg Heil!")
    elif response_id == 2:
        await event.reply(file = "CAADAgADWgADraG3CP76-OQcP7msAg")    # Send a sticker


# Insult
@client.on(events.NewMessage(pattern=re.compile("(love|fuck|screw|damn?) (you|u) Tanya", re.I).search, outgoing=False, forwards=False))
async def insult(event):
    sender = await event.get_sender()
    print([currentTime.strftime("%c")], [sender.id], sender.username, event.pattern_match.string)
    await event.reply(event.pattern_match.group(1)+" you too!")    # "Love you too!"


# Hahahahahaha
@client.on(events.NewMessage(pattern=re.compile("(hah?\w+a)$", re.I).match, outgoing=False))
async def haha(event):
    sender = await event.get_sender()
    response_length = randint(2,5)
    response = event.pattern_match.group(1)*response_length    # Format the response (between 2 to 5 times the original length)
    print([currentTime.strftime("%c")], [sender.id], sender.username, [response_length], event.pattern_match.string)
    if probability(0.2):
        await event.reply(response.capitalize())    # Capitalize the response

# Yes or no
@client.on(events.NewMessage(pattern=re.compile("(yes|y)(/| or )(no|n)\??$").search, outgoing=False, forwards=False))    # Matches "y/n" "yes or no" "yes/no?" etc
async def yes_or_no(event):
    sender = await event.get_sender()
    print([currentTime.strftime("%c")], [sender.id], sender.username, event.pattern_match.string)
    if probability(0.5):
        await event.reply("Yes.")
    else:
        await event.reply("No.")


client.start(bot_token=token)
client.send_message(151462131, "**Bot started at:**  "+currentTime.strftime("`%c`"))
print("Bot started at:  "+currentTime.strftime("%c"))
client.run_until_disconnected()
