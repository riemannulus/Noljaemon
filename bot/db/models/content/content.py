from enum import Enum
from bot.db.base import Base


class ContentType(Enum):
    RAID = 0,
    EXPEDITION_RAID = 1,
    ABYSS_RAID = 2,
    ABYSS_DUNGEON = 3,
    CHALLENGE_ABYSS_DUNGEON = 4,
    CHALLENGE_GUARDIAN = 5


class Content(Base):
    __tablename__ = "content"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String)
    item_level = Column(Integer)