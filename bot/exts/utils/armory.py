from discord import Embed
from discord.ext import commands

from bot.bot import Bot
from bot.crawler.armory import ArmoryCrawler


class Armory(commands.Cog):
    """Getting the latency between the bot and websites."""

    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.session = bot.db_session

    @commands.command(name="전정실")
    async def get_armory(self, ctx: commands.Context) -> None:
        args = ctx.message.content.split(" ")
        username = args[1]

        crawler = ArmoryCrawler(username)
        temporary_message = await ctx.send("전투정보실을 조회중입니다...")
        try:
            characters = crawler.get_characters_name()

            primary_server = ''
            primary_server_char_count = 0

            for server in characters.keys():
                if primary_server_char_count < len(characters[server]):
                    primary_server = server
                    primary_server_char_count = len(characters[server])

            embed = Embed(title=f"[{username}의 전투정보실]")
            for char in characters[primary_server]:
                armory = ArmoryCrawler(char)
                embed.add_field(name=f"<{primary_server}>", value=f"{char}, {armory.get_characters_item_level()}", inline=False)
            await temporary_message.delete()
            await ctx.send(embed=embed)
        except Exception as e:
            await temporary_message.delete()
            await ctx.send(f"올바른 사용자명이 아닙니다.")



def setup(bot: Bot) -> None:
    """Load the Latency cog."""
    bot.add_cog(Armory(bot))
