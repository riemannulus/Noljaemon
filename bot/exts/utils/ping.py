from datetime import datetime

from discord import Embed
from discord.ext import commands

from bot.bot import Bot
from bot.db.models.user import User


DESCRIPTIONS = (
    "Command processing time",
    "Discord API latency"
)
ROUND_LATENCY = 3


class Latency(commands.Cog):
    """Getting the latency between the bot and websites."""

    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.session = bot.db_session

    @commands.command(name="핑")
    async def ping(self, ctx: commands.Context) -> None:
        """
        Gets different measures of latency within the bot.
        Returns bot, Python Discord Site, Discord Protocol latency.
        """
        # datetime.datetime objects do not have the "milliseconds" attribute.
        # It must be converted to seconds before converting to milliseconds.
        bot_ping = (datetime.utcnow() - ctx.message.created_at).total_seconds() * 1000
        if bot_ping <= 0:
            bot_ping = "Your clock is out of sync, could not calculate ping."
        else:
            bot_ping = f"{bot_ping:.{ROUND_LATENCY}f} ms"

        # Discord Protocol latency return value is in seconds, must be multiplied by 1000 to get milliseconds.
        discord_ping = f"{self.bot.latency * 1000:.{ROUND_LATENCY}f} ms"

        embed = Embed(title="Pong!")
        user = User(name="test", discord_id="test2")
        self.session.add(user)
        get_users = self.session.query(User).filter_by(name="test")
        for item in get_users:
            print(item.name)

        for desc, latency in zip(DESCRIPTIONS, [bot_ping, discord_ping]):
            embed.add_field(name=desc, value=latency, inline=False)

        await ctx.send(embed=embed)


def setup(bot: Bot) -> None:
    """Load the Latency cog."""
    bot.add_cog(Latency(bot))
