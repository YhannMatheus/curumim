import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
import asyncio

class BotEvents(commands.Cog):
    def __init__(self, bot):
        load_dotenv()
        self.bot = bot
        self.aviso_channel_id = bot.aviso_channel_id
        super().__init__()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Bot online como {self.bot.user}")
        channel = self.bot.get_channel(self.aviso_channel_id)
        if channel:
            if channel.permissions_for(channel.guild.me).send_messages:
                await channel.send("Bot está online!")
            else:
                print("Sem permissão para enviar mensagens no canal de avisos.")
        else:
            print("Canal de avisos não encontrado.")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        try:
            await member.send(f"Bem-vindo ao servidor, {member.mention}...",
                              f"\nSou o Curumin, seu assistente virtual dentro da Porãygua, pode vir à mim se precisar de algo."
                              f"\nVocê acaba de entrar para nosso grupo de desenvolvimento coletivo, onde podemos entrar ou criar projetos para aprender novas tecnologias"
                              f"\nAqui o unico requisito é ser interessado por aprender e ter o compromisso de agir."
                              f"\nEntre em projetos de outros devs ou crie seu próprio projeto e chame outros para participarem que tenham o mesmo intusiamos que você"
                              f"\n para me chamar use o comando !kajuda, voce receberá por aqui a lista de comandos que poderá receber."
                              f"\nNovamente, **bem vindo ao Porãygua dev goup!!!!🥳🥳**") 
        except discord.Forbidden:
            print(f"Não foi possível enviar mensagem privada para {member.name}")
            guild = member.guild
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                member: discord.PermissionOverwrite(read_messages=True)
            }
            temp_channel = await guild.create_text_channel('bem-vindo', overwrites=overwrites)
            await temp_channel.send(f"Bem-vindo ao servidor, {member.mention}..."
                                    f"\nSou o Curumin, seu assistente virtual dentro da Porãygua, pode vir à mim se precisar de algo."
                                    f"\nVocê acaba de entrar para nosso grupo de desenvolvimento coletivo, onde podemos entrar ou criar projetos para aprender novas tecnologias"
                                    f"\nAqui o unico requisito é ser interessado por aprender e ter o compromisso de agir."
                                    f"\nEntre em projetos de outros devs ou crie seu próprio projeto e chame outros para participarem que tenham o mesmo intusiamos que você"
                                    f"\n para me chamar use o comando !kajuda, voce receberá por aqui a lista de comandos que poderá receber."
                                    f"\nNovamente, **bem vindo ao Porãygua dev goup!!!!🥳🥳**")
            await asyncio.sleep(300)  # Wait for 5 minutes
            await temp_channel.delete()

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        try:
            await member.send(f"Lamentamos que você tenha saído do servidor, {member.mention}. Se mudar de ideia, estaremos sempre aqui para recebê-lo de volta.")
        except discord.Forbidden:
            print(f"Não foi possível enviar mensagem privada para {member.name}")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(f"Comando não encontrado. Por favor, verifique se digitou corretamente, {ctx.author.mention}.")

    @commands.Cog.listener()
    async def on_disconnect(self):
        channel = self.bot.get_channel(self.aviso_channel_id)
        if channel:
            await channel.send("opa, parece que estamos em manutenção, me de uns instantes!!")
        else:
            print("Canal de avisos não encontrado.")

async def setup(bot):
    await bot.add_cog(BotEvents(bot))