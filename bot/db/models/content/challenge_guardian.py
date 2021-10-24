from sqlalchemy import Column, Integer, BigInteger, ForeignKey

from bot.db.models.content.content import Content


class ChallengeGuardian(Content):
    clear_limit_count = 1
    same_content_limit_count = 3
    reset_period_in_day = 7

    __tablename__ = "challenge_guardian"
    id = Column(BigInteger, ForeignKey('content.id'), primary_key=True)
    required_item_level = Column(Integer, nullable=False)
    stage = Column(Integer, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'challenge_guardian',
    }
