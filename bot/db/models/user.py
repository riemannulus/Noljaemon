from sqlalchemy import Column, BigInteger, String
from bot.db.base import Base


class User(Base):
    __tablename__ = "users"
    id = Column(BigInteger, primary_key=True)
    name = Column(String, nullable=False)
    discord_id = Column(String, nullable=False)
