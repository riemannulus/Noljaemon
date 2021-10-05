from sqlalchemy import Column, Integer, String, BigInteger
from bot.db.base import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    discord_id = Column(BigInteger)

    def __repr__(self):
        return self.name
