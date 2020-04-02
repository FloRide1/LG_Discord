import discord

class Party:
    def __init__(self,listPlayers,channels,owner):
        self.owner = owner
        self.listPlayers = listPlayers
        self.channels = channels
        self.choiced = None
        self.number = None
        self.message = [None,None]
        self.lRoles = []
        self.multiple = ["👨‍🌾","🐺"]
        self.roleMax = []
        self.fileString = ["👨‍🌾 Villageois","🔮 Voyante","🏹 Chasseur","🐺 LG","🧹 Witch","❤️ Cupidon"]
        self.listRoles = []
        self.reactionNumber = ["0️⃣","1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣"]

    async def on_configuration_update(self):
        strQ = ""
        print(self.listRoles)
        for i in self.fileString:
            strQ += "\n"
            if (i.split(" ")[0] in self.listRoles):
                if (self.listRoles[self.listRoles.index(i.split(" ")[0])+1]>0):
                    strQ+="+ " + i
                else:
                    strQ += "- " + i 
            else:
                strQ += "- " + i 
        strR = ("```diff\nRoles : {0}/{1}{2}```").format(len(self.lRoles),len(self.listPlayers),strQ)
        if (self.message[0] != None):
            await self.message[0].edit(content = strR)
        else:
            self.message[0] = await self.channels[1].send(strR)
            self.message[1] = await self.channels[1].send("Nombre :")
        for i in self.fileString:
            try :
                await self.message[0].add_reaction((i.split(" ")[0]))
            except :
                None
        for i in self.reactionNumber:
            try :
                await self.message[1].add_reaction(i)
            except :
                None

            
    async def on_character_choice(self,reaction,user):
        if (reaction.message.content != self.message[0].content or reaction.message.author == user):
            return
        if (user != self.owner):
            if (user.dm_channel == None):
                await user.create_dm()
            await reaction.message.remove_reaction(reaction.emoji,user)
            await user.dm_channel.send("Dégage Connard...")
            return
        self.choiced = reaction.emoji
        for i in reaction.message.reactions:
                if (i.emoji != reaction.emoji and i.count>=2):
                    await i.message.remove_reaction(i.emoji,user)
        if (self.number != None):
            if (self.number>2 and not(reaction.emoji in self.reactionNumber)):
                await self.message[1].remove_reaction(self.reactionNumber[self.number],user)
                self.number = None
        else :
            return
        if (self.number != None):
            try:
                self.listRoles[self.listRoles.index(reaction.emoji)+1] = self.number
            except:
                self.listRoles.append(self.choiced)
                self.listRoles.append(self.number)
        await self.on_configuration_update()
        


    async def on_number_choice(self,reaction,user):
        if (reaction.message.content != self.message[1].content or reaction.message.author == user):
            return
        if (user != self.owner):
            if (user.dm_channel == None):
                await user.create_dm()
            await reaction.message.remove_reaction(reaction.emoji,user)
            await user.dm_channel.send("Dégage Connard...")
            return
        if (not(self.choiced in self.multiple) and self.reactionNumber.index(reaction.emoji)>=2):
            await reaction.message.remove_reaction(reaction.emoji,user)
            return
        self.number = self.reactionNumber.index(reaction.emoji)
        for i in reaction.message.reactions:
            if (i.emoji != reaction.emoji and i.count>=2):
                await i.message.remove_reaction(i.emoji,user)
        if (self.choiced != None):
            try:
                self.listRoles[self.listRoles.index(self.choiced)+1] = self.number
            except:
                self.listRoles.append(self.choiced)
                self.listRoles.append(self.number)
        await self.on_configuration_update()

    async def on_character_unchoice(self,reaction,user):
        if (reaction.message.content != self.message[0].content or reaction.message.author == user):
            return
        if (reaction.emoji == self.choiced):
            self.choiced = None
    
    async def on_number_unchoice(self,reaction,user):
        if (reaction.message.content != self.message[1].content or reaction.message.author == user):
            return
        if (reaction.emoji == self.number):
            self.number = None