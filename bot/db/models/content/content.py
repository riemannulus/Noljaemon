from enum import Enum

from sqlalchemy import Column, Integer, BigInteger, String, Enum as EnumType
from sqlalchemy.orm import relationship

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
    id = Column(BigInteger, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(EnumType(ContentType), nullable=False)
    character_contents = relationship('CharacterContent')
