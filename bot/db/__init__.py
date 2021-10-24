from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, Session

import bot.db.base
from bot.db.models.character import *
from bot.db.models.content.content import *
from bot.db.models.content.abyss_dungeon import *
from bot.db.models.content.abyss_raid import *
from bot.db.models.content.challenge_abyss_dungeon import *
from bot.db.models.content.challenge_guardian import *
from bot.db.models.content.content import *
from bot.db.models.content.expedition_raid import *
from bot.db.models.content.raid import *
from bot.db.models.user import *



def create_session(url: str) -> Session:
    engine = create_engine(url)
    base.Base.metadata.create_all(engine, checkfirst=True)
    return scoped_session(sessionmaker(autocommit=False,
                                       autoflush=True,
                                       bind=engine))


instance: Session = None
