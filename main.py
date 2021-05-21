import time
import requests
import importlib
import time
import datetime as dt
import humanize
from config import ownerID,dbUri,dbName,api_id,api_hash,session
from re import sub,findall,split
from telethon.tl.functions.messages import GetMessagesRequest,EditMessageRequest
from telethon.tl.functions.channels import GetMessagesRequest as GetMessagesRequestChannel
from pymongo import MongoClient
from telethon.sync import TelegramClient, events
from telethon.helpers import add_surrogate
from os import path
from telethon.tl.types import Message
client = TelegramClient(session, api_id, api_hash, lang_code="id")
client.plugins = list()
pluginFolder="Plugins"
db = MongoClient(dbUri)[dbName]

#initializing collection.
if "users" not in db.list_collection_names():
    db.create_collection("users")
    print("Collection 'users' created")
if "echos" not in db.list_collection_names():
    db.create_collection("echos")
    print("Collection 'echos' created")
if "afks" not in db.list_collection_names():
    db.create_collection("afks")
    print("Collection 'afks' created")

usersDb = db.users
echosDb = db.echos
afks = db.afks

client.afk = afks
client.db = db
client.users = usersDb
client.ownerID = ownerID
if path.exists(pluginFolder) == False:
    print(f"Folder '{pluginFolder}' tidak dapat ditemukan!")
    exit(0)

def loadPlugins():
    for plugin in path.os.listdir(pluginFolder):
        if plugin.endswith(".py"):
            plugin = plugin.split(".")[0]
            client.plugins.clear() if plugin in client.plugins else None # clear plugins when plugin is already registered
            plg = importlib.import_module(f"{pluginFolder}.{plugin}")
            plg.setup(client)

def findPlugin(pluginOrAlias: str):
    plugin = None
    for pl in client.plugins:
        if pl.name == pluginOrAlias or (pluginOrAlias in pl.aliases):
            plugin = pl
    return plugin


@client.on(events.NewMessage())
async def handlerNeww(event: events.NewMessage.Event):
    if event.message.from_id == None:
        return
    #afk
    #mention
    mentions = findall(r'(?<![@\w])@(\w{1,25})', event.message.message)
    if len(mentions) > 0:
        tagger = await client.get_entity(event.message.from_id.user_id)
        if tagger.bot == True:
            return
        textAFK = f"@{tagger.username}, "
        for mention in mentions:
            userTagged = await client.get_entity(mention)
            taggedAFK = afks.find_one({ "id": userTagged.id })
            if userTagged.bot == False and taggedAFK != None:
                textAFK += f"@{userTagged.username} afk karena `{taggedAFK['reason']}`, "
        await client.send_message(event.chat_id, textAFK, parse_mode="Markdown", reply_to=event.message)
        
    userAFK = afks.find_one({"id":event.message.from_id.user_id})
    if userAFK != None:
        userInfo = await client.get_entity(event.message.from_id.user_id)
        afks.delete_one({"id":event.message.from_id.user_id})
        humanize.i18n.activate("id_ID")
        humanDateAFK = humanize.naturaltime(dt.datetime.fromtimestamp(userAFK['date'])).replace("sekarang", "beberapa saat yang lalu")
        await client.send_message(event.chat_id, f"Selamat datang kembali @{userInfo.username} setelah AFK untuk `{humanDateAFK}`", reply_to=event.message, parse_mode="Markdown")
    #echo
    user = usersDb.find_one({"id":event.message.from_id.user_id})
    if user == None:
        usersDb.insert_one({
            "id":event.message.from_id.user_id,
            "date": round(time.time() * 1000),
            "echo": False
        })
        print(f"Users created #{event.message.from_id.user_id}")
    elif user["echo"] == True and event.message.from_id.user_id != ownerID:
        meEcho = await client.send_message(event.chat_id, event.message, reply_to=event.message)
        echosDb.insert_one({
            "reply_author": event.message.id,
            "reply_me": meEcho.id,
            "chat": event.chat_id
        })

@client.on(events.MessageDeleted)
async def handleDelete(event: events.MessageDeleted.Event):
    deletedMessageDb = echosDb.find_one({"reply_author": event.deleted_id})
    if deletedMessageDb != None:
        await client.delete_messages(deletedMessageDb["chat"], [deletedMessageDb["reply_me"]])
        echosDb.delete_one({"reply_author": deletedMessageDb["reply_author"]})
@client.on(events.MessageEdited)
async def handleEdit(event: events.MessageEdited.Event):
    editedMessageDb = echosDb.find_one({"reply_author":event.message.id})
    if editedMessageDb != None:

        result = await client(GetMessagesRequestChannel(channel=event.input_chat,id=[editedMessageDb["reply_me"]]))
        if len(result.messages) < 1:
            # if message doesn't exist
            echosDb.delete_one({"reply_author":editedMessageDb["reply_author"]})
        else:
            myMessage = result.messages[0]
            await client(EditMessageRequest(
                peer=myMessage.peer_id,
                message=event.message.message,
                id=myMessage.id,
                media=myMessage.media,
                reply_markup=myMessage.reply_markup,
                entities=myMessage.entities,
                no_webpage=True
            ))
loadPlugins() # initializing plugin
@client.on(events.NewMessage(pattern=r'\/\/[a-z](.?)?.*'))
async def handlerNew(event: events.NewMessage.Event):
    args=split(r' +', event.message.message[2:])
    command=args[0].lower()
    plugin = findPlugin(command)
    if plugin == None or (plugin.ownerOnly and event.message.from_id.user_id != ownerID) or (event.message.from_id.user_id == ownerID and event.message.reply_to != None):
        return
    else:
        await plugin.exec(event,args[1:])
        if event.message.from_id.user_id == ownerID: await client.delete_messages(event.chat_id,[event.message.id])

    
client.start()
client.run_until_disconnected()