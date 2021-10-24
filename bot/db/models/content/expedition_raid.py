from sqlalchemy import Column, Integer, BigInteger, ForeignKey

from bot.db.models.content.content import Content


class ExpeditionRaid(Content):
    clear_limit_count = 1
    expedition_limit_count = 1
    reset_period_in_day = 7

    __tablename__ = "expedition_raid"
    id = Column(BigInteger, ForeignKey('content.id'), primary_key=True)
    required_item_level = Column(Integer, nullable=False)
    stage = Column(Integer, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'expedition_raid',
    }
