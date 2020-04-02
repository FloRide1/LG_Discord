import discord

TOKEN = "Njk0ODg2NTE2MTE5NDM3NDEy.XoWMiw.Jxl9y8B6WdQ3EHXfsryMrUWldhk"

class DiscordBot(discord.Client) :
    def __init__(self):
        self.partyIsLaunch = False
        self.listPlayers = []
        self.owner = 0 
        self.channels = []
        super().__init__()
    async def on_guild_join(self,guild):
        self.guild = guild

    async def on_guild_available(self,guild):
        self.guild = guild
    async def on_ready(self):
        print("Bot is Ready")
        print("Name : " + self.user.name)
        print(self.guild)
    
    async def on_message(self,message):
        if (message.author == self.user):
            if (message.content == "Qui veut jouer ?"):
                await message.add_reaction("👍")
                await message.add_reaction("👎")
                await message.add_reaction("▶️")
            return
        
        if (message.content.startswith("lg!play")):
            if (not(self.partyIsLaunch)):
                self.partyIsLaunch = True
                self.listPlayers = []
                self.owner = message.author
                await message.channel.send("Qui veut jouer ?")
            else :
                await message.channel.send("Une partie est déja lancée")

        if (message.content.startswith("lg!end")):
            if (self.owner == message.author):
                self.listPlayers = []
                self.partyIsLaunch = False
                for i in self.channels:
                    await i.delete()
                    del i[0]# <-- Ici
                await message.channel.send("Fin de la partie")
            else :
                await message.channel.send("Vous n'etes pas le MDJ")

    async def on_reaction_add(self,reaction,user):
        if (user == self.user):
            return
        if (reaction.message.content == "Qui veut jouer ?" and reaction.emoji == "👍"):
            self.listPlayers.append(user)
        if (reaction.message.content == "Qui veut jouer ?" and reaction.emoji == "▶️"):
            if (user == self.owner):
                listP = "Liste des joueurs :"
                for i in self.listPlayers:
                    listP+= "\n - " + i.name 
                await reaction.message.channel.send(listP)
                
                category = await self.guild.create_category("Loup Garou - Game")
                self.channels.append(category)
                overwrites = {
                    self.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    self.owner : discord.PermissionOverwrite(read_messages=True)
                }
                chan = await self.guild.create_text_channel(name = "Configuration",category = category,overwrites = overwrites)
                self.channels.append(chan)
                chan = await self.guild.create_text_channel(name = "Village",category = category)
                self.channels.append(chan)
                game = Party(self.listPlayers,self.channels)
                await game.on_configuration_update()
            else :
                await reaction.message.channel.send(user.name + " vous n'etes pas le MDJ")
    async def on_reaction_remove(self,reaction,user):
        if (reaction.message.content == "Qui veut jouer ?" and reaction.emoji == "👍"):
            self.listPlayers.remove(user)



class Party:
    def __init__(self,listPlayers,channels):
        self.listPlayers = listPlayers
        self.channels = channels
        self.lRoles = []

    async def on_configuration_update(self):
        strR = ("Roles : {0}/{1}").format(len(self.lRoles),len(self.listPlayers))
        if (self.channels[1].last_message != None):
            await self.channels[1].last_message.edit(content = strR)
        else:
            await self.channels[1].send(strR)

if __name__ == "__main__":
    DiscordBot().run(TOKEN) 

