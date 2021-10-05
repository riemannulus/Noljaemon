from typing import List

from discord import Embed
from discord.ext import commands

from bot.bot import Bot
from bot.crawler.armory import ArmoryCrawler
from bot.db import User, Character


class Register(commands.Cog):
    """Getting the latency between the bot and websites."""

    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.session = bot.db_session

    def get_all_character_armory(self, username) -> List[ArmoryCrawler]:
        main_char = ArmoryCrawler(username)
        characters = []

        for char_name in main_char.get_all_characters_names('실리안'):
            characters.append(ArmoryCrawler(char_name))

        return characters

    @commands.command(name="업데이트")
    async def update(self, ctx: commands.Context) -> None:
        user = self.session.query(User).filter_by(discord_id=ctx.author.id).first()
        if not user:
            await ctx.send('등록을 먼저 해 주세요.')
            return

        characters = user.characters
        print(characters)
        temporary_message = await ctx.send("캐릭터를 업데이트 중입니다...")

        try:
            for character in characters:
                armory = ArmoryCrawler(character.name)
                character.item_level = armory.get_characters_item_level()

            await temporary_message.delete()
            await ctx.send('업데이트에 성공했습니다.')

        except Exception as e:
            print(e)
            await temporary_message.delete()
            await ctx.send('업데이트에 실패했습니다.')
        self.session.commit()


    @commands.command(name="등록")
    async def registration(self, ctx: commands.Context) -> None:
        args = ctx.message.content.split(" ")
        username = args[1]

        if self.session.query(User).filter_by(discord_id=ctx.author.id).first():
            await ctx.send('이미 등록이 완료 된 계정입니다.')
            return

        temporary_message = await ctx.send("유저를 등록중입니다...")
        user = User(name=ctx.author.name, discord_id=ctx.author.id)
        self.session.add(user)

        characters = self.get_all_character_armory(username)

        try:
            embed = Embed(title=f"[{ctx.author.name}의 등록이 완료되었습니다]")
            for character in characters:
                char_model = Character(
                    server='실리안',
                    name=character.username,
                    job=character.get_characters_job(),
                    item_level=character.get_characters_item_level(),
                    user=user)

                embed.add_field(name=f"{char_model.name}", value=f"아이템 Lv: {char_model.item_level}", inline=True)
                self.session.add(char_model)

            self.session.commit()
            await temporary_message.delete()
            await ctx.send(embed=embed)

        except Exception as e:
            print(e)
            await temporary_message.delete()
            await ctx.send('등록에 실패했습니다.')


def setup(bot: Bot) -> None:
    """Load the Latency cog."""
    bot.add_cog(Register(bot))
