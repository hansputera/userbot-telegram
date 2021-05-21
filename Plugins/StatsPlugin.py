import os
import psutil
import humanize
from telethon.sync import TelegramClient,events

class StatsCommand:
    def __init__(self, bot: TelegramClient):
        self.client = bot
        self.name = "stats"
        self.description = "Stats command"
        self.aliases = ["st","botinfo"]
        self.ownerOnly = False
    async def exec(self, event: events.NewMessage.Event,args:[str]):
        me = await self.client.get_me()
        _load1, _load5, load15 = psutil.getloadavg()
        used = humanize.naturalsize(psutil.virtual_memory().used)
        total = humanize.naturalsize(psutil.virtual_memory().total)
        cpu_usage = (load15/os.cpu_count()) * 100
        dbtxt=""
        for col in self.client.db.list_collection_names():
            docs = self.client.db[col].find()
            dbtxt += f"{col} ({len(docs)}) | "
        await self.client.send_message(event.chat_id, f"- ID: `{me.id}`\n- Username: @{me.username}\n- Plugins: `{len(self.client.plugins)} plugin(s)`\n- CPU Usage: `{round(cpu_usage,3)}%`\n- RAM Usage: `{psutil.virtual_memory().percent}% ({used} / {total})`\n- DB Stats: {dbtxt}", parse_mode="Markdown",reply_to=event.message)


def setup(bot):
    command = StatsCommand(bot)
    bot.plugins.append(command)
    print(f"{__name__} initialized")