from sqlalchemy import Column, Integer, BigInteger, ForeignKey

from bot.db.models.content.content import Content


class ChallengeAbyssDungeon(Content):
    clear_limit_count = 1
    same_content_limit_count = 2
    expedition_limit_count = 2
    reset_period_in_day = 7

    __tablename__ = "challenge_abyss_dungeon"
    id = Column(BigInteger, ForeignKey('content.id'), primary_key=True)
    required_item_level = Column(Integer, nullable=False)
    stage = Column(Integer, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'challenge_abyss_dungeon',
    }
