import sys
from telethon.sync import TelegramClient,events

class EvalCommand:
    def __init__(self, bot:TelegramClient):
        self.client = bot
        self.name = "eval"
        self.description = "Evaluate python code"
        self.aliases = ["ev","evaluate","evalit"]
        self.ownerOnly = True
    async def exec(self, event: events.NewMessage.Event, args: [str]):
        if args == []:
            await self.client.send_message(event.chat_id, "Masukin code ularnya beb")
        else:
            txt = " ".join(args)
            try:
                code = compile(txt,"<string>","eval")
                await self.client.send_message(event.chat_id,f"`{eval(code)}`",parse_mode="Markdown",reply_to=event.message)
            except Exception as e:
                await self.client.send_message(event.chat_id, f"`{e}`",parse_mode="Markdown",reply_to=event.message)

def setup(bot):
    command = EvalCommand(bot)
    bot.plugins.append(command)
    print(f"{__name__} initialized")