from app import db
from app.result.models import Result

class Player(db.Model):
    __tablename__ = 'playerTable'

    player_id = db.Column(db.Integer, primary_key=True)
    playerName = db.Column(db.String(80), unique=True)
    playerPassword = db.Column(db.String(80))
    soloRank = db.Column(db.Integer)
    teamRank = db.Column(db.Integer)
    winResult = db.relationship('Result', backref='winPlayer', lazy='dynamic')
    loseResult = db.relationship('Result', backref='losePlayer', lazy='dynamic')



    def __init__(self, playerName, password):
        self.playerName = playerName
        self.playerPassword = password

    def __repr__(self):
        return '<User %r>' % (self.playerName)

    def getId(self):
        return self.player_id

    def setSoloRank(self, rank):
        self.rank = rank

    def getSoloRank(self):
        rank = self.soloRank
        if rank is 4:
            return "major"
        if rank is 3:
            return "Triple A"
        if rank is 2:
            return "Double A"
        if rank is 1:
            return "beginner"
