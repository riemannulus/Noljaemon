from sqlalchemy import Column, BigInteger, String, ForeignKey
from sqlalchemy.orm import relationship

from bot.db.base import Base


class Character(Base):
    __tablename__ = "character"
    id = Column(BigInteger, primary_key=True)
    server = Column(String, nullable=False)
    name = Column(String, nullable=False)
    job = Column(String, nullable=False)
    item_level = Column(BigInteger, nullable=False)
    character_contents = relationship('CharacterContent')


class CharacterContent(Base):
    __tablename__ = "character_content"
    is_cleared = Column(BigInteger, nullable=False)
    character_id = Column(BigInteger, ForeignKey('character.id'), primary_key=True)
    content_id = Column(BigInteger, ForeignKey('content.id'), primary_key=True)

