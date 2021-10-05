import enum

from sqlalchemy import Column, Integer, String, Enum
from bot.db.base import Base


class ContentResetCycleEnum(enum.Enum):
    daily = "일간"
    weekly = "주간"


class ContentDependentTypeEnum(enum.Enum):
    expedition = "원정대"
    character = "캐릭터"


class Content(Base):
    __tablename__ = "contents"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    dependent_type = Column(Enum(ContentDependentTypeEnum))
    reset_cycle = Column(Enum(ContentResetCycleEnum))
    item_level = Column(Integer)
    discord_icon = Column(String)

    def __repr__(self):
        return self.name
