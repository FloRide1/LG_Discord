import discord
from party import *

async def on_launch_message(self,message):
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
            self.channels = [] 
            await message.channel.send("Fin de la partie")
        else :
            await message.channel.send("Vous n'etes pas le MDJ")

async def on_launch_reaction_add(self,reaction,user):
    if (user == self.user):
        return
        
    if (reaction.message.content == "Qui veut jouer ?" and reaction.emoji == "👍"):
        self.listPlayers.append(user) 
        try :
            await reaction.message.remove_reaction("👎",user)
            return
        except discord.HTTPException:
            return  
    if (reaction.message.content == "Qui veut jouer ?" and reaction.emoji == "👎"):
        try :
            await reaction.message.remove_reaction("👍",user)
            return
        except discord.HTTPException:
            return  
    if (reaction.message.content == "Qui veut jouer ?" and reaction.emoji == "▶️"):
        if (user == self.owner):
            listP = "Liste des joueurs :"
            for i in self.listPlayers:
                listP+= "\n - " + i.name 
            await reaction.message.channel.send(listP)
            if (self.channels == []):
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
                self.game = Party(self.listPlayers,self.channels,self.owner)
            await self.game.on_configuration_update()
            
        else :
            if (user.dm_channel == None):
                await user.create_dm()
            await user.dm_channel.send(user.name + " vous n'etes pas le MDJ")
        await reaction.message.remove_reaction(emoji = reaction.emoji,member = user)
    await self.game.on_character_choice(reaction,user)
    await self.game.on_number_choice(reaction,user)
    

        

async def on_launch_reaction_rem(self,reaction,user):
        if (reaction.message.content == "Qui veut jouer ?" and reaction.emoji == "👍"):
            self.listPlayers.remove(user)
        await self.game.on_character_unchoice(reaction,user)
        await self.game.on_number_unchoice(reaction,user)