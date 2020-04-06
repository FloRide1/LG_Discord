from utils import *

class Manage:
    def __init__(self,owner,guild,channel,bot):
        self.owner = owner
        self.guild = guild
        self.channel = channel
        self.message = {}
        self.bot = bot
        self.unique = bot.unique
        self.choiced = None
        self.number = None
        self.character = {
                            "Villageois"    : {'emoji' : '👨‍🌾', 'multiple' : 1, 'number' : 0},
                            "Voyante"       : {'emoji' : '🔮', 'multiple' : 0, 'number' : 0},
                            "Chasseur"      : {'emoji' : '🏹', 'multiple' : 0, 'number' : 0},
                            "Loup Garou"    : {'emoji' : '🐺', 'multiple' : 1, 'number' : 0},
                            "Sorciere"      : {'emoji' : '🧹', 'multiple' : 0, 'number' : 0},
                            "Cupidon"       : {'emoji' : '❤️', 'multiple' : 0, 'number' : 0}
                        }
        self.numbers = ["0️⃣","1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣"]

    async def on_configuration_update(self):
        if (self.message.get('Configuration') == None):
            Configuration = await self.channel.send("Wait Please")
            await add_unique_reaction(Configuration,"allroles",self.unique)
            self.message['Configuration'] = Configuration.id
        else :
            Configuration = await self.channel.fetch_message(self.message['Configuration'])
        message = self.create_configuration_message()
        await Configuration.edit(content = message)
        if (self.message.get('Number') == None):
            Number = await self.channel.send("Number")
            await add_unique_reaction(Number,"number",self.unique)
            self.message['Number'] = Number.id
        

    async def on_message(self,message):
        author = message.author
        content = message.content
        if (content.startswith("lg!stop") or content.startswith("lg!end")):
            if (message.author == self.owner):
                await self.bot.on_end()
            else : 
                if (author.dm_channel == None):
                    await author.create_dm()    
                await author.dm_channel.send("Vous n'avez pas l'autorisation d'arreter la partie")
            return
        
    async def on_reaction_add(self,reaction,user):
        message = reaction.message
        if (user != self.owner):
            if (user.dm_channel == None):
                    await user.create_dm()  
            await user.dm_channel.send("Admin = Pas admis ici sauf si MDJ")
            return
        if (message.id == self.message.get('Configuration')):
            await self.on_character_add(reaction,user)
        if (message.id == self.message.get('Number')):
            await self.on_number_add(reaction,user)

    async def on_character_add(self,reaction,user):
        for i in self.character:
            if (self.character[i]['emoji'] == reaction.emoji):
                self.choiced = i
        await self.reaction_isupdate(user)
                
    async def on_number_add(self,reaction,user):
        self.number = self.numbers.index(reaction.emoji)
        await self.reaction_isupdate(user)

    async def reaction_isupdate(self,user):
        if (self.choiced != None and self.number!=None):
            if (self.number < 2 or self.character[self.choiced]['multiple']):
                self.character[self.choiced]['number'] = self.number
                await self.on_configuration_update()
            else:
                Numbermsg = await self.channel.fetch_message(self.message['Number'])
                for i in Numbermsg.reactions:
                    await Numbermsg.remove_reaction(i.emoji,user)

    def create_configuration_message(self):
        message = "```diff\nRoles :"
        character = self.character
        for i in character:
            message += "\n"
            if (character[i]['number']>0):
                message+= "+ " + str(i) + str(character[i]['emoji']*character[i]['number'])
            else :
                message+= "- " + str(i) + str(character[i]['emoji'])
        message+= "```"
        return message
