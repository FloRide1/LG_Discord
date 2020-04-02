import discord

class Party:
    def __init__(self,listPlayers,channels,owner):
        self.owner = owner
        self.listPlayers = listPlayers
        self.channels = channels
        self.choiced = None
        self.number = None
        self.message = [None,None]
        self.multiple = ["👨‍🌾","🐺"]
        self.roleMax = []
        self.fileString = ["👨‍🌾 Villageois","🔮 Voyante","🏹 Chasseur","🐺 LG","🧹 Witch","❤️ Cupidon"]
        self.listRoles = []
        self.reactionNumber = ["0️⃣","1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣"]

    async def on_configuration_update(self):
        
        strQ = ""
        #print(self.listRoles)
        for i in self.fileString:
            strQ += "\n"
            if (i.split(" ")[0] in self.listRoles):
                number = self.listRoles[self.listRoles.index(i.split(" ")[0])+1]
                if (number>0):
                    strQ+="+ " + i
                    if number>=2:
                        strQ+= "×" + str(number)
                else:
                    strQ += "- " + i
            else:
                strQ += "- " + i 
        number = 0
        for i in range(int(len(self.listRoles)/2)):
            number+= self.listRoles[2*i+1]
        strR = ("```diff\nRoles : {0}/{1}{2}```").format(number,len(self.listPlayers),strQ)
        if (number == len(self.listPlayers)):
            try :
                await self.message[0].add_reaction("▶️")
            except :
                None
        else :
            try:
                await self.message[0].remove_reaction("▶️",self.message[0].author)
            except :
                None
        
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
        if (reaction.emoji == "▶️"):
            await self.message[0].delete()
            await self.message[1].delete()
            message = await reaction.message.channel.send("Voulez montrer la configuration aux autres joueurs ?")
            await message.add_reaction("👍")
            await message.add_reaction("👎")
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
        if (self.number != None and self != 0 and self.choiced != None):
            if (self.choiced in self.listRoles):
                self.listRoles[self.listRoles.index(self.choiced)+1] = self.number
            else:
                self.listRoles.append(self.choiced)
                self.listRoles.append(self.number)
            await self.on_configuration_update()
        elif (self.number == 0):
            if (self.choiced in self.listRoles):
                index = self.listRoles.index(self.choiced)
                del self.listRoles[index]
                del self.listRoles[index]
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
        if (self.choiced != None and self.number != 0):
            if (self.choiced in self.listRoles):
                self.listRoles[self.listRoles.index(self.choiced)+1] = self.number
            else:
                self.listRoles.append(self.choiced)
                self.listRoles.append(self.number)
            await self.on_configuration_update()
        elif (self.number == 0):
            if (self.choiced in self.listRoles):
                index = self.listRoles.index(self.choiced)
                del self.listRoles[index]
                del self.listRoles[index]
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