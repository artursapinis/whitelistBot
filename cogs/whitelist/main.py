import logging
import json
import dislash
from discord.ext import commands
from dislash import slash_command, Option, OptionType


class Commands(commands.Cog):
    def __init__(self, bot):
        logging.info('\t\t\tBot [WHITELIST] started!')
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info('cogs.whitelist.main ON_READY')

    @slash_command(description='Whitelist',
                   options=[Option('adress', description='address', type=OptionType.STRING, required=True)])
    @dislash.has_role(902671766156095549)
    async def whitelist(self, ctx, adress = None):
        with open("resources/whitelist.json", "r+") as whitelist:
            data = json.load(whitelist)
            data.append(adress)
            whitelist.seek(0)
            json.dump(data, whitelist)

        await ctx.send('geageag')


def setup(bot):
    bot.add_cog(Commands(bot))
