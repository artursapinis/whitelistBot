import discord
from discord.ext import commands
from dislash import InteractionClient, ContextMenuInteraction, application_commands
import logging


client = commands.Bot(command_prefix='.')
test_guilds = [902669584274964500]
slash_client = InteractionClient(client, test_guilds=test_guilds)

logging.basicConfig(level=logging.INFO)

cog_extensions = (
    'cogs.whitelist.main',
)

cog_extensions_loaded = 0

logging.info('|-------------------- LOADING EXTENSIONS --------------------|')

started_extensions = []
failed_extensions = []

for extension in cog_extensions:
    try:
        client.load_extension(extension)
        logging.info(f'\t\t\tExtension [{extension}] status - STARTED')
        started_extensions.append(extension)
        cog_extensions_loaded += 1
    except Exception as e:
        logging.exception(e)
        logging.exception(f'\t\t\tExtension [{extension}] status - FAILED\n')
        failed_extensions.append(extension)

logging.info(
    f'|----------------- DONE [started {cog_extensions_loaded} out of {len(cog_extensions)}] -----------------|')


@client.event
async def on_ready():
    logging.info('on_ready event called successfully')


@client.event
async def on_slash_command_error(inter: ContextMenuInteraction, error):
    if isinstance(error, application_commands.errors.MissingRole):
        await inter.respond('ERROR', ephemeral=True)

client.run('OTAyNjY5NjY2NTIxMDcxNjQ4.YXhyow.vYID5eDY92ZVi74pUk0amAkEe2E')
