from telethon.sync import TelegramClient,events

class DropCollectionCommand:
    def __init__(self, bot: TelegramClient):
        self.client = bot
        self.name = "drop-collection"
        self.description = "DropCollection command"
        self.aliases = ["dropcol","dropc"]
        self.ownerOnly = True
    async def exec(self, event: events.NewMessage.Event,args:[str]):
        if args == []:
            await self.client.send_message(event.chat_id, "`Masukin nama collectionnya ayang<3`",reply_to=event.message,parse_mode="Markdown")
        else:
            col = args[0].lower()
            if col not in self.client.db.list_collection_names():
                await self.client.send_message(event.chat_id, f"Collection `{col}` tidak dapat ditemukan!",reply_to=event.message,parse_mode="Markdown")
            else:
                self.client.db[col].drop()
                await self.client.send_message(event.chat_id, f"Collection `{col}` dropped!",reply_to=event.message,parse_mode="Markdown")
def setup(bot):
    command = DropCollectionCommand(bot)
    bot.plugins.append(command)
    print(f"{__name__} initialized")