import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot {bot.user.name} jest gotowy.')

@bot.command(name='clear', help='Kasuje podaną ilość wiadomości z kanału. Użycie: clear <liczba>')
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    if amount < 1:
        await ctx.send('Liczba wiadomości do skasowania musi być większa niż 0.')
        return
    deleted = await ctx.channel.purge(limit=amount)
    await ctx.send(f'Skasowano {len(deleted)} wiadomości.', delete_after=5)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('Nie masz odpowiednich uprawnień, aby użyć tej komendy.')
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Proszę podać liczbę wiadomości do skasowania.')
    elif isinstance(error, commands.BadArgument):
        await ctx.send('Proszę podać prawidłową liczbę.')

bot.run(TOKEN)
