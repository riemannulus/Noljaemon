from discord import Embed
from discord.ext import commands, tasks
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from bot.bot import Bot
from bot.crawler.armory import ArmoryCrawler

DESCRIPTIONS = (
    "오레하 프라바사",
    "쿠크세이튼 리허설",
    "발탄 노말",
    "비아키스 노말",
    "아브렐슈드 데자뷰",
    "발탄 하드",
    "비아키스 하드",
    "쿠크세이튼 노말",
    "아브렐슈드 노말 1-2관문",
    "아브렐슈드 노말 3-4관문",
    "아브렐슈드 노말 5-6관문"
)

ITEM_LEVEL_RANGE = (
    1325,
    1385,
    1415,
    1430,
    1430,
    1445,
    1460,
    1475,
    1490,
    1500,
    1520
)

SCHEDULE = AsyncIOScheduler()


class Raid(commands.Cog):
    """Getting the latency between the bot and websites."""

    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.session = bot.db_session

    def start_scheduled(self):
        # SCHEDULE.add_job(self.reset_db, CronTrigger(second='2'))
        # SCHEDULE.start()
        pass

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        self.start_scheduled()

    async def reset_db(self) -> None:
        print('finish')

    @commands.command(name="레이드")
    async def message(self, ctx: commands.Context) -> None:
        args = ctx.message.content.split(" ")
        username = args[1]

        crawler = ArmoryCrawler(username)
        item_level = crawler.get_characters_item_level()

        embed = Embed(title=f"[{username}의 가능 레이드]", colour=0x00a86b)
        for desc, level in zip(DESCRIPTIONS, ITEM_LEVEL_RANGE):
            embed.add_field(name=desc, value=f"{'가능' if item_level >= level else '불가능'}", inline=True)

        await ctx.send(embed=embed)

def setup(bot: Bot) -> None:
    """Load the Latency cog."""
    bot.add_cog(Raid(bot))
