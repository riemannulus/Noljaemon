from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from bot.db.base import Base


class Character(Base):
    __tablename__ = "character"
    id = Column(Integer, primary_key=True)
    server = Column(String)
    name = Column(String)
    job = Column(String)
    item_level = Column(Integer)
    character_contents = relationship('CharacterContent')


class CharacterContent(Base):
    __tablename__ = "character_content"
    is_cleared = Column(BigInteger, nullable=False)
    character_id = Column(BigInteger, ForeignKey('character.id'), primary_key=True)
    content_id = Column(BigInteger, ForeignKey('content.id'), primary_key=True)

