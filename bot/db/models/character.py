from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, Float
from sqlalchemy.orm import relationship, backref

from bot.db.base import Base
from bot.db.models.user import User
from bot.db.models.content.content import Content


class Character(Base):
    __tablename__ = "characters"
    id = Column(Integer, primary_key=True)
    server = Column(String)
    name = Column(String)
    job = Column(String)
    item_level = Column(Float)

    user_id = Column(ForeignKey(User.id))
    user = relationship(
        User,
        backref=backref('characters')
    )

    def __repr__(self):
        return f"{self.name}-{self.job}: {self.item_level}"


class CharacterContent(Base):
    __tablename__ = "contents_by_character"

    character_id = Column(Integer, ForeignKey(Character.id), primary_key=True)
    content_id = Column(Integer, ForeignKey(Content.id), primary_key=True)
    created_at = Column(DateTime, server_default=func.now())

    character = relationship(Character, backref="content")
    content = relationship(Content, backref="character")

    def __repr__(self):
        return f"{self.content.name} - {self.character.name} / {self.created_at}"
