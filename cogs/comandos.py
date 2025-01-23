import os
import discord
import datetime
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands

class BotCommands(commands.Cog):
    def __init__(self, bot):
        load_dotenv()
        self.bot = bot
        super().__init__()

    @commands.command()
    async def ajuda(self, ctx: commands.Context):
        """
        Função que manda uma mensagem para o usuario dos comandos existentes
        """
        await ctx.message.delete()
        await ctx.author.send('Aparentemente você solicitou ajuda, aqui estão algumas funções que você pode realizar....'
                              '\n\n- !kprojeto : lista os projetos em aberto dentro do nosso servidor'
                              '\n- !kajuda : se você já está lendo isso, já sabe pra que serve'
                              '\n- !kmkprojeto : cria uma rquisição de projetos para os adms avaliarem seu projeto'
                              '\n      |->parametros: <nome do projeto> <descrição>'
                              '\n- !kgit : manda o link do git publico da porãygua para você'
                              '\n- !kwtz : envia para você um link para a comunidade do wtzp'
                              '\n- !kreuniao: cria um tiket temporário de texto para conversar em particular com os ADMs do servidor')
    
    @commands.command()
    async def mkprojeto(self,ctx:commands.Context, nome:str, *descricao:str):
        """
        função para solicitar a abertura de um novo projeto
        """
        await ctx.message.delete()
        autor = ctx.author.name
        chanel =  ctx.guild.get_channel(id = 1331459186021634088)
        embed = discord.Embed(title=f"requisição de projeto: {nome}",description=f"{descricao}\nfeito por{autor}")
        
        await chanel.send(embed=embed)

    @commands.command()
    async def wtz(self,ctx:commands.Context):
        ctx.message.delete()
        await ctx.author.send("Opa, o link para nossa comunidade do WhatsApp é esse: \nhttps://chat.whatsapp.com/Hsbwue8gjym9m1LWS4Dfy3\nTe espero lá!!!")

    @commands.command()
    async def git(self,ctx:commands.Context):
        ctx.message.delete()
        await ctx.author.send("Égua mano, ainda não recebi o git da administração, assim que eu tiver eu avido no canal!!")

    @commands.command()
    async def listar_categorias(self, ctx: commands.Context):
        """
        Lista os nomes das categorias do servidor que não começam com "--"
        """
        categorias = [category.name for category in ctx.guild.categories if not category.name.startswith("--")]
        if categorias:
            await ctx.author.send("Projetos:\n" + "\n".join(categorias))
        else:
            await ctx.author.send("Não há projetos abertos no nosso servidor")

    @commands.command()
    async def reuniao(self, ctx: commands.Context):
        """
        Cria um ticket de reunião que dura no máximo 24 horas para falar com um administrador.
        Apenas administradores e o usuário que solicitou podem ler o ticket.
        """
        ctx.message.delete()
        guild = ctx.guild
        author = ctx.author

        # Create a category for tickets if it doesn't exist
        category = discord.utils.get(guild.categories, name="Tickets")
        if not category:
            category = await guild.create_category("Tickets")

        # Create a text channel for the ticket
        ticket_channel = await guild.create_text_channel(f"ticket-{author.name}", category=category)

        # Set permissions for the ticket channel
        await ticket_channel.set_permissions(author, read_messages=True, send_messages=True)
        await ticket_channel.set_permissions(guild.default_role, read_messages=False)
        for role in guild.roles:
            if role.permissions.administrator:
                await ticket_channel.set_permissions(role, read_messages=True, send_messages=True)

        # Send a message in the ticket channel
        await ticket_channel.send(f"{author.mention}, este é o seu ticket de reunião. Um administrador estará com você em breve.")

        # Delete the ticket channel after 24 hours
        await discord.utils.sleep_until(datetime.datetime.utcnow() + datetime.timedelta(hours=24))
        await ticket_channel.delete()


    #!  ADM FUNÇÕES -------
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def novo_projeto(self, ctx: commands.Context, nome: str, member: discord.Member, *descricao: str):
        """
        Cria uma categoria com o nome do projeto + 1 canal de texto forum + 1 canal de voz reunião.
        Dá ao membro direitos totais sobre a categoria e posta um embed no canal de avisos do servidor.
        Somente o autor, com a autorização, poderá entrar nos canais ou ceder a role do projeto a outros usuários.
        """
        ctx.message.delete()
        guild = ctx.guild
        category = await guild.create_category(nome)
        text_channel = await guild.create_text_channel(f'{nome}-forum', category=category)
        voice_channel = await guild.create_voice_channel(f'{nome}-reuniao', category=category)

        await ctx.message.delete()

        # Create a role for the project and assign it to the member
        role = await guild.create_role(name=nome)
        await member.add_roles(role)

        # Set permissions for the category and channels
        await category.set_permissions(member, manage_channels=True, manage_permissions=True, manage_messages=True, connect=True, speak=True)
        await category.set_permissions(guild.default_role, read_messages=False)
        await text_channel.set_permissions(role, read_messages=True, send_messages=True)
        await voice_channel.set_permissions(role, connect=True, speak=True)
        
        embed = discord.Embed(title=f"Novo Projeto - {nome.title()}",
                              description=f"O projeto **{nome}** foi criado e atribuído a {member.mention}.\n\nDescrição: {' '.join(descricao)}",
                              color=discord.Color.green())
        embed.set_thumbnail(member.avatar.url)
        
        await guild.system_channel.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def excluir_projeto(self, ctx: commands.Context, nome: str):
        """
        Exclui a categoria, todos os canais associados a um projeto e a role correspondente.
        """
        ctx.message.delete()
        guild = ctx.guild
        category = discord.utils.get(guild.categories, name=nome)
        role = discord.utils.get(guild.roles, name=nome)
        
        await ctx.message.delete()
        
        if category:
            for channel in category.channels:
                await channel.delete()
            await category.delete()
            if role:
                await role.delete()
            await ctx.send(f"O projeto **{nome}** foi excluído com sucesso.")
        else:
            await ctx.send(f"Categoria **{nome}** não encontrada.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def apagar_reuniao(self, ctx: commands.Context):
        """
        Apaga o ticket de reunião no qual o comando foi escrito.
        Apenas administradores podem usar este comando.
        """
        ctx.message.delete()
        ticket_channel = ctx.channel

        if ticket_channel.category and ticket_channel.category.name == "Tickets":
            await ticket_channel.delete()
            await ctx.send(f"O ticket **{ticket_channel.name}** foi apagado com sucesso.")
        else:
            await ctx.send("Este comando só pode ser usado em um canal de ticket.")


async def setup(bot):
    await bot.add_cog(BotCommands(bot))