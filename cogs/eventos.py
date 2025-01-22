import os
import discord
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands

class BotEvents(commands.Cog):
    def __init__(self, bot):
        load_dotenv()
        self.bot = bot
        super().__init__()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Bot online como {self.bot.user}")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        try:
            await member.send(f"Bem-vindo ao servidor, {member.mention}...",
                              f"\nSou o kurumin, seu assistente virtual dentro da Porãygua, pode vir à mim se precisar de algo.",
                              f"\nVocê acaba de entrar para nosso grupo de desenvolvimento coletivo, onde podemos entrar ou criar projetos para aprender novas tecnologias",
                              f"\nAqui o unico requisito é ser interessado por aprender e ter o compromisso de agir.",
                              f"\nEntre em projetos de outros devs ou crie seu próprio projeto e chame outros para participarem que tenham o mesmo intusiamos que você",
                              f"\n para me chamar use o comando !kajuda, voce receberá por aqui a lista de comandos que poderá receber.",
                              f"\nNovamente, bem vindo ao Porãygua dev goup!!!!🥳🥳") 
        except discord.Forbidden:
            print(f"Não foi possível enviar mensagem privada para {member.name}")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        try:
            await member.send(f"Lamentamos que você tenha saído do servidor, {member.mention}. Se mudar de ideia, estaremos sempre aqui para recebê-lo de volta.")
        except discord.Forbidden:
            print(f"Não foi possível enviar mensagem privada para {member.name}")


      
async def setup(bot):
    await bot.add_cog(BotEvents(bot))