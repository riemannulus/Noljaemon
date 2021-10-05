from sqlalchemy import Column, Integer, String
from bot.db.base import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    discord_id = Column(String)
