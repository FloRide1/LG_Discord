import discord
from manage import *

class Guild:
    def __init__(self,guild):
        self.guild = guild
        self.Manage = None
        self.Channels = {}
        self.unique = {}
        print("Guild is create")
    
    async def on_end(self):
        for i in self.Channels.values():
            await i.delete()
        del self.Manage
        self.Manage = None
        self.unique = []

    async def on_message(self,message):
        content = message.content
        if (content.startswith("lg!start") or content.startswith("lg!play")):
            print("Start || Play as been Detected on : " + self.guild.name)
            if (self.Manage == None):
                owner = message.author
                overwrites = {
                    self.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    owner : discord.PermissionOverwrite(read_messages=True)
                }
                self.Channels['Category'] = await self.guild.create_category("Loup Garou - Game #")
                self.Channels['Manage'] = await self.guild.create_text_channel(name = "management",overwrites = overwrites ,category = self.Channels['Category'])
                await self.delete_doublon_channel()
                self.Manage = Manage(owner,self.guild,self.Channels['Manage'],self)
                await self.Manage.on_configuration_update()
            else : 
                await message.channel.send("Une partie est déja en cours")
            return
        if (message.channel.name == "management"):
            await self.Manage.on_message(message)
            return
    async def on_reaction_add(self,reaction,user):
        message = reaction.message
        if (message.author == user):
            return
        if (message.id in self.unique.keys()):
            self.unique[message.id] = reaction.emoji
            for i in message.reactions:
                if (i.emoji != self.unique[message.id]):
                    await message.remove_reaction(i.emoji,user)
        if (message.channel.name == "management"):
            await self.Manage.on_reaction_add(reaction,user)
            return

    async def delete_doublon_channel(self):
        dictionnaire = self.Channels
        values = dictionnaire.values()
        name = {}
        for i in values:
            name[i.name] = i
        #print("dict :" + str(dictionnaire) + " values : " + str(values) + " Channels : " + str(self.guild.channels))
        for i in self.guild.channels:
            if (name.get(i.name) != None and name.get(i.name) != i):
                await i.delete()
