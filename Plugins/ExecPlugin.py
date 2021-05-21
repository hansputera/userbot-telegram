import subprocess
from telethon.sync import TelegramClient,events

class ExecCommand:
    def __init__(self, bot: TelegramClient):
        self.client = bot
        self.name = "exec"
        self.description = "Execute system"
        self.aliases = ["execute"]
        self.ownerOnly = True
    async def exec(self, event: events.NewMessage.Event,args:[str]):
        if args == []:
            await self.client.send_message(event.chat_id, "Masukin bash command nya sayang<3")
        else:
            loading = await self.client.send_message(event.chat_id, "`Loading, please wait ...`", reply_to=event.message,parse_mode="Markdown")
            try:
                output = subprocess.run(args, check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True)
                if output.stderr:
                    await self.client.edit_message(loading, f"**Error:**\n\n```{output.stderr}```", parse_mode="Markdown")
                else:
                    await self.client.edit_message(loading, f"**Success:**\n\n```{output.stdout}```",parse_mode="Markdown")
            except Exception as e:
                await self.client.edit_message(loading, f"`{e}`", parse_mode="Markdown")

def setup(bot):
    command = ExecCommand(bot)
    bot.plugins.append(command)
    print(f"{__name__} initialized")