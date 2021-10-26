import logging
import json

import discord
import dislash
from discord.ext import commands
from dislash import slash_command, Option, OptionType
import sqlite3


class Commands(commands.Cog):
    def __init__(self, bot):
        logging.info('\t\t\tBot [WHITELIST] started!')
        self.bot = bot
        self.con = sqlite3.connect('resources/database.db')
        c = self.con.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id STRING)''')
        c.close()

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info('cogs.whitelist.main ON_READY')

    @slash_command(description='The list')
    @dislash.is_owner()
    async def list(self, ctx):
        user = await self.bot.fetch_user(ctx.author.id)
        await user.send(file=discord.File('resources/whitelist.json'))

    @slash_command(description='Whitelist',
                   options=[Option('adress', description='address', type=OptionType.STRING, required=True)])
    @dislash.has_role(902671766156095549)
    async def whitelist(self, ctx, adress = None):
        if not adress.startswith('0x'):
            return await ctx.send('Your message must start with 0x', ephemeral=True)

        c = self.con.cursor()
        r = c.execute(f'SELECT EXISTS(SELECT 1 FROM users WHERE user_id=?)', (ctx.author.id, ))
        f = r.fetchone()[0]
        if f == 1:
            return await ctx.send('You already used this command!', ephemeral=True)

        with open("resources/whitelist.json", "r+") as whitelist:
            data = json.load(whitelist)
            data.append(adress)
            whitelist.seek(0)
            json.dump(data, whitelist)
            execute = f'INSERT INTO users (user_id) VALUES({str(ctx.author.id)})'
            c.execute(execute)
            self.con.commit()

        c.close()
        await ctx.send('Registered!', ephemeral=True)


def setup(bot):
    bot.add_cog(Commands(bot))
