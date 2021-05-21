# Telegram UserBOT
UserBOT telegram created with telethon using MTProto.

# Commands
- AFK (`//afk [reason]`) - `Gives your status that AFK`
- Echo (Only Owner, `//echo @some1`) - `Will repeat every user message that has been activated.`
- Exec (Only Owner, `//exec <bash_command>`) - `Execute bash command`
- Eval (Only Owner, `//eval <python_code>`) - `Executing python language`
- Stats (`//stats`) - `Userbot statistics`
- Ping (`//ping`) - `Testing the request rate to telegram website`
- Drop Collection (Only Owner, `//dropc <collection_name>`) - `Delete the collection from the database.`

# Requirements
- [PyMongo](https://pypi.org/pypi/pymongo)
- [MongoDB](https://mongodb.org)
- [Telethon](https://pypi.org/pypi/telethon)
- [Humanize](https://pypi.org/pypi/humanize)
- [DNSPython](https://pypi.org/pypi/dnspython) (If using MongoDB SRV)