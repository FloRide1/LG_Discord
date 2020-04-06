import discord
from guild import *

class DiscordBot(discord.Client):
    def __init__(self):
        self.Guilds = []
        super().__init__()

    async def on_ready(self):
        print("Bot is Ready")

    async def on_guild_join(self,guild):
        self.Guilds.append(Guild(guild))
        print("New Guild as invite the Bot : " + guild.name)

    async def on_guild_available(self,guild):
        self.Guilds.append(Guild(guild))
        print("New Guild is available : " + guild.name)

    async def on_message(self,message):
        for i in self.Guilds:
            if message.guild == i.guild:
                await i.on_message(message)
                return

    async def on_reaction_add(self,reaction,user):
        for i in self.Guilds:
            if reaction.message.guild == i.guild:
                await i.on_reaction_add(reaction,user)
                return