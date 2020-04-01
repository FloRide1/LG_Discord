import discord

TOKEN = "Njk0ODg2NTE2MTE5NDM3NDEy.XoSgtw.LxN4m7fznpB8r8JNo_QO4SPs3yA"

class DiscordBot(discord.Client) :
    def __init__(self):
        super().__init__()
        
    async def on_ready(self):
        print("Bot is Ready")
        print("Name : " + self.user.name)
    
    async def on_message(self,message):
        if (message.author == self.user):
            if (message.content == "Qui veut jouer ?"):
                await message.add_reaction("👍")
                await message.add_reaction("👎")
            return
        
        if (message.content.startswith("lg!")):
            await message.channel.send("Qui veut jouer ?")
    async def on_reaction_add(self,reaction,user):
        if (user.author == self.user)
            return
        print(user.name)
        



if __name__ == "__main__":
    DiscordBot().run(TOKEN) 