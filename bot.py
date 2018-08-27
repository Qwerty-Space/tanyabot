from telethon import TelegramClient, sync, events, logging, custom
logging.basicConfig(level=logging.WARNING)
import re
import os
path = os.path
# getenv = os.getenv
from random import randint
from datetime import datetime
import configparser
# from dotenv import load_dotenv
# load_dotenv()

### VARIABLES ###
config = configparser.ConfigParser()
config.read_file(open("config.ini"))
token = config['DEFAULT']['TOKEN']
session_name = config['DEFAULT']['SESSION_NAME']
api_id = config['DEFAULT']['ID']
api_hash = config['DEFAULT']['HASH']

script_dir = path.dirname(path.realpath(__file__))
print(script_dir)
currentTime = datetime.now()


### LOG IN TO TELEGRAM ##
print("Connecting...")

client = TelegramClient(path.join(script_dir, session_name), api_id, api_hash)


# Probability
def probability(percent):
    probability = randint(0, 99) < percent
    print(probability)
    return probability


# /start
@client.on(events.NewMessage(pattern = "(/start)$"))
async def on_start(event):
    sender = (await event.get_sender())
    if event.is_private:
        print([currentTime.strftime("%c")], [sender.id], sender.username, event.pattern_match.string)
        await event.respond('This is a bot for silly replies')


# Hi, Hungry!
@client.on(events.NewMessage(pattern = "(?i)^(?:i'?m|i am) ((?:\S+ ?){1,3})$", outgoing=False, forwards=False))
async def i_am_dad(event):
    sender = (await event.get_sender())
    print([currentTime.strftime("%c")], [sender.id], sender.username, event.pattern_match.string)
    if probability(20):
        await event.reply("Hi " + event.pattern_match.group(1))


# MEIN FÜHRER!
@client.on(events.NewMessage(pattern = re.compile("(hitler|führer|fuhrer)", re.I).search, outgoing=False))
async def mein_fuhrer(event):
    sender = (await event.get_sender())
    response_id = randint(0,2)
    print([currentTime.strftime("%c")], [sender.id], sender.username, [response_id], event.pattern_match.string)
    if response_id == 0:
        await event.reply("Heil Hitler!")
    elif response_id == 1:
        await event.reply("Sieg Heil!")
    elif response_id == 2:
        await event.reply(file = "CAADAgADWgADraG3CP76-OQcP7msAg")


# Insult
@client.on(events.NewMessage(pattern = re.compile("(love|fuck|screw|damn?) (you|u) Tanya", re.I).search))
async def insult(event):
    print([currentTime.strftime("%c")], [sender.id], sender.username, event.pattern_match.string)
    await event.reply(event.pattern_match.group(1)+" you too!")


# hahahahahaha
@client.on(events.NewMessage(pattern = re.compile("(hah?\w+a)$", re.I).match))
async def haha(event):
    sender = (await event.get_sender())
    response_length = randint(2,5)
    print([currentTime.strftime("%c")], [sender.id], sender.username, [response_length], event.pattern_match.string)
    if probability(20):
        await event.reply(event.pattern_match.group(1)*response_length)


client.start(bot_token=token)
client.send_message(151462131, "**Bot started at:**  "+currentTime.strftime("`%c`"))
print("Bot started at:  "+currentTime.strftime("%c"))
client.run_until_disconnected()
