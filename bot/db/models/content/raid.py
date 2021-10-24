from sqlalchemy import String, Column, Integer, BigInteger, ForeignKey

from bot.db.models.content.content import Content


class Raid(Content):
    clear_limit_count = 1
    same_content_limit_count = 3
    reset_period_in_day = 7

    __tablename__ = "raid"
    id = Column(BigInteger, ForeignKey('content.id'), primary_key=True)
    difficulty = Column(String, nullable=False)
    required_item_level = Column(Integer, nullable=False)
    stage = Column(Integer, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'raid',
    }
