import discord

TOKEN = "Njk0ODg2NTE2MTE5NDM3NDEy.XoS0hQ.2AR27Alth1pT39tyr9OB3snGDxI"

class DiscordBot(discord.Client) :
    def __init__(self):
        self.partyIsLaunch = False
        self.partyPlayer = []
        self.owner = 0 
        super().__init__()
        
    async def on_ready(self):
        print("Bot is Ready")
        print("Name : " + self.user.name)
    
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
                self.partyPlayer = []
                self.owner = message.author.name
                await message.channel.send("Qui veut jouer ?")
            else :
                await message.channel.send("Une partie est déja lancée")

        if (message.content.startswith("lg!end")):
            if (self.owner == message.author.name):
                self.partyPlayer = []
                self.partyIsLaunch = False
                await message.channel.send("Fin de la partie")
            else :
                await message.channel.send("Vous n'etes pas le MDJ")

    async def on_reaction_add(self,reaction,user):
        if (user == self.user):
            return
        if (reaction.message.content == "Qui veut jouer ?" and reaction.emoji == "👍"):
            self.partyPlayer.append(user.name)
        if (reaction.message.content == "Qui veut jouer ?" and reaction.emoji == "▶️"):
            if (user.name == self.owner):                
                await reaction.message.channel.send("Liste des joueurs :\n - " + "\n - ".join(self.partyPlayer))
            else :
                await reaction.message.channel.send(user.name + " vous n'etes pas le MDJ")
    async def on_reaction_remove(self,reaction,user):
        if (reaction.message.content == "Qui veut jouer ?" and reaction.emoji == "👍"):
            self.partyPlayer.remove(user.name)
        

if __name__ == "__main__":
    DiscordBot().run(TOKEN) 