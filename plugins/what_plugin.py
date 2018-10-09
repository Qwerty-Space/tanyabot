r"""When a user says "wot" the bot will reply with the previous message in BOLD CAPS.

pattern:  `(?i)^wh?[aou]t\??$`
"""

from telethon import events, sync

# Can't you hear?!
@events.register(events.NewMessage(pattern=r"(?i)^wh?[aou]t\??$"))
async def wut(event):
    if event.is_reply:
        repliedmsg = await event.get_reply_message()
        msgtext = repliedmsg.raw_text
    else:
        prev_id = (event.id)-1
        prev_msg = await event.client.get_messages(event.chat_id, ids=prev_id)
        msgtext = prev_msg.raw_text
    if msgtext:
        await event.reply(f"**{msgtext.upper()}**")
        sender = await event.get_sender()
        print(f"[{event.date.strftime('%c')}] [{sender.id}] {sender.username}: {event.pattern_match.string}")
