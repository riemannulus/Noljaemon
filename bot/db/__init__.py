import bot.db.base

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, Session

from bot.db.models.user import *
from bot.db.models.character import *


def create_session(url: str) -> Session:
    engine = create_engine(url)
    base.Base.metadata.create_all(engine, checkfirst=True)
    return scoped_session(sessionmaker(autocommit=False,
                                autoflush=True,
                                bind=engine))

instance: Session = None
