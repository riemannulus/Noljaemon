from sqlalchemy import Column, Integer, String
from bot.db.base import Base


class Content(Base):
    __tablename__ = "content"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String)
    item_level = Column(Integer)