import time
import requests
from telethon.sync import TelegramClient,events

class PingCommand:
    def __init__(self, bot: TelegramClient):
        self.client = bot
        self.name = "ping"
        self.description = "Ping command"
        self.aliases = ["pong"]
        self.ownerOnly = False
    async def exec(self, event: events.NewMessage.Event,args:[str]):
        awal = time.monotonic() * 1000
        requests.get("https://core.telegram.org")
        akhir = time.monotonic() * 1000
        await self.client.send_message(event.chat_id, f"Pong!! `{round(akhir-awal,3)} ms`",reply_to=event.message,parse_mode="Markdown")

def setup(bot):
    command = PingCommand(bot)
    bot.plugins.append(command)
    print(f"{__name__} initialized")