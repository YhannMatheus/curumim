import os
import discord
import datetime
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands

class BotCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        load_dotenv()
        self.bot = bot
        self.aviso_channel_id = bot.aviso_channel_id
        super().__init__()

    @commands.command()
    async def ajuda(self, ctx: commands.Context):
        """
        Função que manda uma mensagem para o usuario dos comandos existentes
        """
        await ctx.message.delete()
        await ctx.author.send('Aparentemente você solicitou ajuda, aqui estão algumas funções que você pode realizar....'
                              '\n\n- !kprojetos : lista os projetos em aberto dentro do nosso servidor'
                              '\n- !kajuda : se você já está lendo isso, já sabe pra que serve'
                              '\n- !pedir : cria uma rquisição de projetos para os adms avaliarem seu projeto'
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
    async def projeto(self, ctx: commands.Context):
        """
        Lista os nomes dos projetos ainda abertos dentro da Porãygua
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
        await ctx.message.delete()
        guild = ctx.guild
        author = ctx.author

        # Create a category for tickets if it doesn't exist
        category = discord.utils.get(guild.categories, name="--Tickets")
        if not category:
            category = await guild.create_category("--Tickets")

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

    @commands.command()
    async def pedir(self,ctx:commands.Context,nome:str, *descricao:str):
        """
        função para solicitar a abertura de um novo projeto
        """
        await ctx.message.delete()
        autor = ctx.author.name
        chanel =  ctx.guild.get_channel(id = 1333840477971021884)
        embed = discord.Embed(title=f"requisição de projeto: {nome}",description=f"{descricao}\nfeito por{autor}")
        
        await chanel.send(embed=embed)


    #!  ADM FUNÇÕES -------
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def abrir(self, ctx: commands.Context, nome: str, member: discord.Member, *descricao: str):
        """
        Cria uma categoria com o nome do projeto + 1 canal de texto forum + 1 canal de voz reunião.
        Dá ao membro direitos totais sobre a categoria e posta um embed no canal de avisos do servidor.
        Somente o autor, com a autorização, poderá entrar nos canais ou ceder a role do projeto a outros usuários.
        """
        await ctx.message.delete()
        guild = ctx.guild

        # Cria a categoria e os canais
        category = await guild.create_category(nome)
        text_channel = await guild.create_text_channel(f'{nome}-forum', category=category)
        voice_channel = await guild.create_voice_channel(f'{nome}-reuniao', category=category)

        # Cria uma role para o projeto e atribui ao membro
        role = await guild.create_role(name=nome)
        await member.add_roles(role)

        # Define permissões para a categoria e canais
        await category.set_permissions(member, manage_channels=True, manage_permissions=True, manage_messages=True, connect=True, speak=True)
        await category.set_permissions(role, read_messages=True, send_messages=True, connect=True, speak=True)
        await category.set_permissions(guild.default_role, read_messages=False)
        await text_channel.set_permissions(role, read_messages=True, send_messages=True)
        await voice_channel.set_permissions(role, connect=True, speak=True)

        # Limita a descrição a 2048 caracteres (limite do Discord para a descrição de um embed)
        descricao_str = ' '.join(descricao)
        if len(descricao_str) > 2048:
            descricao_str = descricao_str[:2045] + '...'

        # Cria o embed
        embed = discord.Embed(
            title=f"Novo Projeto - {nome.title()}",
            description=f"O projeto **{nome}** foi criado e atribuído a {member.mention}.\n\nDescrição: {descricao_str}",
            color=discord.Color.green()
        )

        # Envia o embed para o canal de avisos
        aviso_channel = self.bot.get_channel(self.bot.aviso_channel_id)
        if aviso_channel:
            if aviso_channel.permissions_for(aviso_channel.guild.me).send_messages:
                await aviso_channel.send(embed=embed)
                print(f"Embed enviado para o canal de avisos: {aviso_channel.name}")
            else:
                print("Sem permissão para enviar mensagens no canal de avisos.")
        else:
            print("Canal de avisos não encontrado.")
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def aviso(self,ctx:commands.Context, titulo:str,*texto:str):
        
        descricao_str = ' '.join(texto)
        if len(descricao_str) > 2048:
            descricao_str = descricao_str[:2045] + '...'

        embed = discord.Embed(title=f"Aviso - {titulo}",
                              description=f"{descricao_str}",
                              color=discord.Color.green())
        
        aviso_channel = self.bot.get_channel(self.bot.aviso_channel_id)
        
        if aviso_channel:
            if aviso_channel.permissions_for(aviso_channel.guild.me).send_messages:
                await aviso_channel.send(embed=embed)
                print(f"Embed enviado para o canal de avisos: {aviso_channel.name}")
            else:
                print("Sem permissão para enviar mensagens no canal de avisos.")
        else:
            print("Canal de avisos não encontrado.")
        
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def del_projeto(self, ctx: commands.Context, nome: str):
        """
        Exclui a categoria, todos os canais associados a um projeto e a role correspondente.
        """
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
    async def encerrar(self, ctx: commands.Context):
        """
        Apaga o ticket de reunião no qual o comando foi escrito.
        Apenas administradores podem usar este comando.
        """
        await ctx.message.delete()
        ticket_channel = ctx.channel

        if ticket_channel.category and ticket_channel.category.name == "--Tickets":
            await ticket_channel.delete()
            await ctx.send(f"O ticket **{ticket_channel.name}** foi apagado com sucesso.")
        else:
            await ctx.send("Este comando só pode ser usado em um canal de ticket.")


async def setup(bot):
    await bot.add_cog(BotCommands(bot))