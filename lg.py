import discord

class Bot(discord.Client):
    
    def __init__ (self):
        super().__init__()

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self, message):
        
        if(message.author == self.user):
            return
        if(message.content.startswith("lg!Jouer")):
            await message.channel.send("Bonjour et bienvenue à Thiercelieux, combien de joueurs êtes vous?")

## Test envoie dm

        if(message.content.startswith("lg!dm")):

            member = discord.utils.get(message.guild.members, name=message.content.split(" ")[1])

            try:
                await member.send("Bienvenue dans le test Loup Garou")
            except discord.Forbidden:
                await message.channel.send("Le joueur " + str(member) + " dois activer ses messages privés")
            except AttributeError:
                await message.channel.send("Le joueur " + str(member) + " n'est pas dans le village")
            

if __name__ == "__main__":

    Loup_Garou_1 = Bot()
    Loup_Garou_1.run("Njk0NTc1NTU3MDQzNTUyMzA3.XoSC_A.hJPwWxEhxyVoQZm0KWtk79nH7Ko")