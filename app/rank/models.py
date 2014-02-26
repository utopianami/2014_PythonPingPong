from app import db

class Rank(db.Model):
    __tablename__ = 'rankTable'

    id = db.Column(db.String(80), primary_key=True)
    rank = db.Column(db.String(80))

    def getRank(self, rank):
        self.rank = rank

