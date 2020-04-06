async def add_unique_reaction(message,typeEmoji,unique,listPers = None):
    dictEmoji = {}
    dictEmoji['foragainst'] = ["👍","👎"]
    dictEmoji['allroles'] = ["👨‍🌾","🔮","🏹","🐺","🧹","❤️"]
    dictEmoji['number'] = ["0️⃣","1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣"]
    if (dictEmoji.get(typeEmoji) != None):
        for i in dictEmoji[typeEmoji]:
            await message.add_reaction(i)
    else:
        for i in listPers:
            await message.add_reaction(i)
    unique[message.id] = "last"