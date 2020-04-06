import discord
from party import *
from partyLaunch import *

TOKEN = "Njk0ODg2NTE2MTE5NDM3NDEy.XocNfQ.rccy2KbcU8LE1MOQw8X68W3J1bA"

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
        #print("Name : " + self.user.name)
        #print(self.guild)
    
    async def on_message(self,message):
        await on_launch_message(self,message)
    async def on_reaction_add(self,reaction,user):
        await on_launch_reaction_add(self,reaction,user)
            
    async def on_reaction_remove(self,reaction,user):
        await on_launch_reaction_rem(self,reaction,user)
        

if __name__ == "__main__":
    DiscordBot().run(TOKEN) 

