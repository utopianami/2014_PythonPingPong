from sqlalchemy import Enum
from app import db

class Rank(db.Model, Enum):
    __tablename__ = 'rankTable'

    MAJOR = 4
    AAA = 3
    AA = 2
    A = 1
    id = db.Column(db.String(80), primary_key=True)
    rank = db.Column(db.String(80))

    def getRank(self, rank):
        self.rank = rank

