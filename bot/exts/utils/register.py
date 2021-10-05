from discord import Embed
from discord.ext import commands

from bot.bot import Bot


class Register(commands.Cog):
    """Getting the latency between the bot and websites."""

    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.session = bot.db_session

    @commands.command(name="등록")
    async def registration(self, ctx: commands.Context) -> None:
        args = ctx.message.content.split(" ")
        username = args[1]

        embed = Embed(title=f"[{username}의 등록이 완료되었습니다]")
        embed.add_field(name=f"{username}", value=f"아이템 Lv: {1490}", inline=True)
        embed.add_field(name=f"{username}", value=f"아이템 Lv: {1491}", inline=True)
        embed.add_field(name=f"{username}", value=f"아이템 Lv: {1492}", inline=True)
        embed.add_field(name=f"{username}", value=f"아이템 Lv: {1493}", inline=False)

        await ctx.send(embed=embed)


def setup(bot: Bot) -> None:
    """Load the Latency cog."""
    bot.add_cog(Register(bot))
