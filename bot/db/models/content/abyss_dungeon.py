from sqlalchemy import Column, Integer, BigInteger, ForeignKey, String

from bot.db.models.content.content import Content


class AbyssDungeon(Content):
    clear_limit_count = 1
    reset_period_in_day = 7

    __tablename__ = "abyss_dungeon"
    id = Column(BigInteger, ForeignKey('content.id'), primary_key=True)
    difficulty = Column(String, nullable=False)
    required_item_level = Column(Integer, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'content_dungeon',
    }
