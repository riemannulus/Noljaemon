import asyncio
import datetime
from typing import Dict, List

from discord import Embed, Emoji
from discord.ext import commands, tasks
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy import and_, or_

from bot.bot import Bot
from bot.crawler.armory import ArmoryCrawler
from bot.db import Content, User, Character, CharacterContent
from bot.db.models.content.content import ContentDependentTypeEnum

RAID_LIST = (
    "아르고스",
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

EMOJI_LIST = (
    1325,
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


def get_start_of_week_day_from_the_target_date(target_date: datetime.datetime) -> datetime.datetime:
    delta = target_date.weekday()
    if delta < 2:
        delta += 7

    return target_date - datetime.timedelta(days=delta-2)


def get_end_of_week_day_from_the_target_date(target_date: datetime.datetime) -> datetime.datetime:
    return get_start_of_week_day_from_the_target_date(target_date) + datetime.timedelta(days=6)


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

    async def get_raid_info(self, char: Character) -> dict:
        now = datetime.datetime.now()
        start_of_weekday = get_start_of_week_day_from_the_target_date(now)
        end_of_weekday = get_end_of_week_day_from_the_target_date(now)
        cleared_contents = self.session.query(CharacterContent) \
            .join(Character) \
            .join(User) \
            .filter(
            and_(
                User.id == char.user.id,
                and_(
                    start_of_weekday < CharacterContent.created_at,
                    CharacterContent.created_at < end_of_weekday
                )
            )).all()

        cleared_contents_dict = {}
        for cleared_content in cleared_contents:
            if cleared_content.content.name in cleared_contents_dict:
                cleared_contents_dict[cleared_content.content.name].append(cleared_content.character)
            else:
                cleared_contents_dict[cleared_content.content.name] = [cleared_content.character]

        all_contents = self.session.query(Content).all()

        cleared_info = {}
        for content in all_contents:
            cleared_info[content.name] = self.check_is_cleared(cleared_contents_dict, content, char)

        return cleared_info

    def check_is_cleared(self, cleared_contents_dict: Dict, content: Content, char: Character) -> bool:
        # 캐릭터가 해당 컨텐츠를 플레이 할 수 없는 경우에도 클리어 완료한 것으로 본다.
        # FIXME: 나중에 컨텐츠를 플레이 할 수 있고 클리어 한 것인지 플레이 자체가 불가능한 것인지를 구분해야 할 때 이 부분 수정할 것.
        if char.item_level < content.item_level:
            return True

        if content.dependent_type == ContentDependentTypeEnum.character:
            if content.name in cleared_contents_dict:
                cleared_char_list = cleared_contents_dict[content.name]
                if char in cleared_char_list:
                    return True
        elif content.dependent_type == ContentDependentTypeEnum.expedition:
            if content.name in cleared_contents_dict:
                return True

        return False

    async def lookup_with_char(self, ctx: commands.Context, char_name: str):
        char = self.session.query(Character).filter_by(name=char_name).first()

        if not char:
            await ctx.send('등록을 먼저 해 주세요.')
            return

        embed = Embed(title=f"[{char.name}의 가능 레이드]", colour=0x00a86b)
        raid_info = await self.get_raid_info(char)

        for (name, cleared) in raid_info.items():
            embed.add_field(name=name, value=f"{'X' if cleared else 'O'}", inline=True)

        return embed

    async def lookup_without_char(self, ctx: commands.Context):
        user = self.session.query(User).filter_by(discord_id=ctx.author.id).first()
        if not user:
            await ctx.send('등록을 먼저 해 주세요.')
            return

        embed = Embed(title=f"[{ctx.author.name}의 가능 레이드]", colour=0x00a86b)
        for character in user.characters:
            cleared_info = await self.get_raid_info(character)
            cleared_list = [f"{info[0]}: {'X' if info[1] else 'O'}" for info in cleared_info.items()]
            cleared_list_str = '\n'.join(cleared_list)
            embed.add_field(
                name=character.name,
                value=cleared_list_str,
                inline=True)
        return embed

    async def find_contents(self, emoji: Emoji):
        emoji_str = str(emoji)

        return self.session.query(Content).filter_by(discord_icon=emoji_str).all()

    async def update_db_cleared_raid(self, contents: List[Content], char: Character):
        for content in contents:
            char_content = CharacterContent(character=char, content=content)
            self.session.add(char_content)
        self.session.commit()

    async def update_cleared_raid(self, ctx: commands.Context, char_name: str):
        char = self.session.query(Character).filter_by(name=char_name).first()

        if not char:
            await ctx.send('등록되지 않은 캐릭터입니다.')
            return

        def check(reaction, user):
            return user == ctx.author

        contents = self.session.query(Content).all()
        embed = Embed()
        text_list = [f"{content.name}: {content.discord_icon}" for content in contents]
        embed.add_field(name=f"[{char_name}(이)가 클리어한 레이드를 선택해주세요]", value='\n'.join(text_list))

        text = await ctx.send(embed=embed)
        for content in contents:
            await text.add_reaction(content.discord_icon)

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
            cleared_contents = await self.find_contents(reaction.emoji)
            await self.update_db_cleared_raid(cleared_contents, char)
            await text.delete()
            result = ", ".join([str(c) for c in cleared_contents])
            await ctx.send(f"{result} 의 클리어 등록이 완료되었습니다.")

        except asyncio.TimeoutError:
            await ctx.send('시간이 초과되었습니다.')

    @commands.command(name="레이드")
    async def message(self, ctx: commands.Context) -> None:
        args = ctx.message.content.split(" ")
        if len(args) == 1:
            embed = await self.lookup_without_char(ctx)
        elif len(args) == 2:
            embed = await self.lookup_with_char(ctx, args[1])
        else:
            await ctx.send('잘못된 명령어입니다.')
            embed = None

        if not embed:
            return

        await ctx.send(embed=embed)

    @commands.command(name="클리어")
    async def cleared(self, ctx: commands.Context) -> None:
        args = ctx.message.content.split(" ")
        if len(args) != 2:
            await ctx.send('잘못된 명령어입니다. (예: !클리어 구의동최고미남손병기씨)')
            return

        await self.update_cleared_raid(ctx, args[1])


def setup(bot: Bot) -> None:
    """Load the Latency cog."""
    bot.add_cog(Raid(bot))
