import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import asyncio

# Carregar variáveis do .env
load_dotenv()
DISCORD_TOKEN = os.getenv("TOKEN")

if DISCORD_TOKEN is None:
    raise ValueError("DISCORD_TOKEN não foi encontrado no arquivo .env")

# Definir o ID do canal de avisos
AVISO_CHANNEL_ID = 1331459186021634088

# Configurar o bot
permisoes = discord.Intents.default()
permisoes.guilds = True
permisoes.members = True
permisoes.message_content = True

# Adicionar permissões necessárias
permisoes.messages = True
permisoes.reactions = True

bot = commands.Bot(command_prefix="!k", intents=permisoes)

# Passar o ID do canal de avisos para os cogs
bot.aviso_channel_id = AVISO_CHANNEL_ID

async def load_cogs():
    for arquivo in os.listdir('cogs'):
        if arquivo.endswith(".py") and not arquivo.startswith("__"):
            await bot.load_extension(f"cogs.{arquivo[:-3]}")

async def main():
    await load_cogs()
    await bot.start(DISCORD_TOKEN)

if __name__ == "__main__":
    asyncio.run(main())