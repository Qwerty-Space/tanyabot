from telethon import events, sync, custom

# Can't you hear?!
@events.register(events.NewMessage(pattern=r"(?i)^wh?[aou]t\??$"))
async def wut(event):
    if event.is_reply:
        sender = await event.get_sender()
        print(f"[{event.date.strftime('%c')}] [{sender.id}] {sender.username}: {event.pattern_match.string}")
        repliedmsg = await event.get_reply_message()
        await event.reply(f"**{repliedmsg.text.upper()}**", reply_to=event.reply_to_msg_id)
