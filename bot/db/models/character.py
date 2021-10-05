from sqlalchemy import Column, Integer, String
from bot.db.base import Base


class Character(Base):
    __tablename__ = "character"
    id = Column(Integer, primary_key=True)
    server = Column(String)
    name = Column(String)
    job = Column(String)
    item_level = Column(Integer)

class CharacterContent(Base):
    __tablename__ = "character_content"

