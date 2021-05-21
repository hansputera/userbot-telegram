from datetime import datetime, timezone
from telethon.sync import TelegramClient,events

class AFKCommand:
    def __init__(self, bot: TelegramClient):
        self.client = bot
        self.name = "afk"
        self.description = "AFK command"
        self.aliases = ["aepka"]
        self.ownerOnly = False
    async def exec(self, event: events.NewMessage.Event,args:[str]):
        reason = "Busy"
        if len(args) > 0:
            reason = " ".join(args)
        user = await self.client.get_entity(event.message.from_id.user_id)
        self.client.afk.insert_one({
            "id": event.message.from_id.user_id,
            "date": datetime.now(timezone.utc).timestamp(),
            "reason": reason
        })
        await self.client.send_message(event.chat_id, f"@{user.username} AFK, karena `{reason}`", parse_mode="Markdown",reply_to=event.message)

def setup(bot):
    command = AFKCommand(bot)
    bot.plugins.append(command)
    print(f"{__name__} initialized")