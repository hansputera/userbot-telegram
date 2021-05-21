from time import time
from telethon.tl.functions.users import GetUsersRequest
from telethon.sync import TelegramClient,events
from re import sub

class EchoCommand:
    def __init__(self, bot: TelegramClient):
        self.client = bot
        self.name = "echo"
        self.description = "Echo command"
        self.aliases = ["replay"]
        self.ownerOnly = True
    async def exec(self, event: events.NewMessage.Event,args:[str]):
        # reply_to=event.message.reply_to
        # if reply_to == None:
        #     await self.client.send_message(event.chat_id, "`Mohon reply message seseorang >_<`", reply_to=event.message, parse_mode="Markdown")
        # else:
        #     message = await self.client(GetMessagesRequest(id=[reply_to.reply_to_msg_id]))
        #     print(message.messages[0].from_id)
        if args == []:
            await self.client.send_message(event.chat_id, "`Masukin username`", reply_to=event.message,parse_mode="Markdown")
        else:
            try:
                username = args[0]
                users = await self.client(GetUsersRequest(id=[sub('@','',username)]))
                if len(users) < 1:
                    await self.client.send_message(event.chat_id, "`Tidak ditemukan!`", parse_mode="Markdown",reply_to=event.message)
                user = users[0]
                if user.id == self.client.ownerID:
                    return
                userInDb = self.client.users.find_one({"id":user.id})
                if userInDb == None:
                    self.client.users.insert_one({
                        "id":user.id,
                        "date": time() * 1000,
                        "echo": True
                    })
                    await self.client.send_message(event.chat_id, f"{username} echo telah dinyalakan",reply_to=event.message)
                else:
                    textNyala = "dinyalakan" if userInDb["echo"] == False else "dimatikan"
                    self.client.users.update_one({"id":user.id},{"$set":{"echo": True if userInDb["echo"] == False else False}})
                    await self.client.send_message(event.chat_id,f"{username} echo telah {textNyala}",reply_to=event.message)
            except Exception as e:
                await self.client.send_message(event.chat_id, f"`{e}`", parse_mode="Markdown",reply_to=event.message)

            
def setup(bot):
    command = EchoCommand(bot)
    bot.plugins.append(command)
    print(f"{__name__} initialized")