import logging
import json
from io import StringIO
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
        c.execute(
            '''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id STRING, address STRING)''')
        c.close()

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info('cogs.whitelist.main ON_READY')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if not message.content == '.list':
            return

        if not message.guild:
            try:
                guild = await self.bot.fetch_guild(896294632353304616)

                if message.author.id == guild.owner_id:
                    c = self.con.cursor()
                    r = c.execute('SELECT * FROM users').fetchall()
                    c.close()
                    data = {}
                    for user in r:
                        data[str(user[1])] = user[2]

                    file = discord.File(fp=StringIO(json.dumps(data, indent=3)), filename='whitelist.json')
                    await message.channel.send(file=file)

            except discord.errors.Forbidden:
                pass
        else:
            pass

    @slash_command(description='Whitelist',
                   options=[Option('address', description='address', type=OptionType.STRING, required=True)])
    @dislash.has_role(902919803034013726)
    async def whitelist(self, ctx, address=None):
        if not address.startswith('0x'):
            return await ctx.send(':red_circle: Your address must start with 0x', ephemeral=True)

        try:
            c = self.con.cursor()
            r = c.execute(f'SELECT EXISTS(SELECT 1 FROM users WHERE user_id=?)', (str(ctx.author.id),))
            f = r.fetchone()[0]
            if f == 1:
                update = f"UPDATE users SET address = '{address}' WHERE user_id = {str(ctx.author.id)}"
                c.execute(update)
                self.con.commit()
                c.close()
                return await ctx.send(f':white_check_mark: You changed your address to: **{address}**', ephemeral=True)
            c.execute(f'INSERT INTO users (user_id, address) VALUES("{str(ctx.author.id)}", "{address}")')
            self.con.commit()
            c.close()
            await ctx.send(f':white_check_mark: Registered! Address: **{address}**', ephemeral=True)
        except BaseException as e:
            logging.exception(e)
            await ctx.send(':red_circle: Something went wrong! Try again!', ephemeral=True)

    @slash_command(description='Info about your whitelist!')
    @dislash.has_role(902919803034013726)
    async def info(self, ctx):
        try:
            c = self.con.cursor()
            r = c.execute(f'SELECT EXISTS(SELECT 1 FROM users WHERE user_id=?)', (str(ctx.author.id),))
            f = r.fetchone()[0]
            if f == 1:
                get_user_address = f'SELECT address FROM users WHERE user_id=?'
                c.execute(get_user_address, (str(ctx.author.id),))
                resp = c.fetchall()[0][0]
                return await ctx.send(f':green_circle: Your current address is: **{resp}**', ephemeral=True)
        except BaseException as e:
            logging.exception(e)
            await ctx.send(':red_circle: Something went wrong! Try again!', ephemeral=True)


def setup(bot):
    bot.add_cog(Commands(bot))
