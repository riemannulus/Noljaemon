import discord

from discord.ext import commands
from sqlalchemy.orm import scoped_session, Session

from bot import constants
from bot import db


class Bot(commands.Bot):
    db_session: Session

    def __init__(self, command_prefix, *args, db_url, **kwargs):
        super().__init__(command_prefix, *args, **kwargs)
        self.load_database(db_url)

    @classmethod
    def create(cls) -> "Bot":
        """Create and return an instance of a Bot."""

        intents = discord.Intents.all()
        intents.presences = False
        intents.dm_typing = False
        intents.dm_reactions = False
        intents.invites = False
        intents.webhooks = False
        intents.integrations = False

        if constants.Bot.debug:
            db_url = "sqlite:///:memory:"
        else:
            db_url = constants.get_db_url()

        return cls(
            command_prefix=commands.when_mentioned_or(constants.Bot.prefix),
            case_insensitive=True,
            max_messages=10_000,
            intents=intents,
            db_url=db_url
        )

    def load_extensions(self) -> None:
        from bot.utils.extensions import EXTENSIONS

        extensions = set(EXTENSIONS)  # Create a mutable copy.

        for extension in extensions:
            self.load_extension(extension)

    def load_database(self, url) -> scoped_session:
        db.instance = db.create_session(url)
        self.db_session = db.instance
        return self.db_session
