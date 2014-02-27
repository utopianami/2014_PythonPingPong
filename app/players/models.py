from app import db
from app.result.models import Result

class Player(db.Model):
    __tablename__ = 'playerTable'

    player_id = db.Column(db.Integer, primary_key=True)
    playerName = db.Column(db.String(80), unique=True)
    playerPassword = db.Column(db.String(80))
    soloRank = db.Column(db.Integer)
    teamRank = db.Column(db.Integer)

    def __init__(self, playerName, password):
        self.playerName = playerName
        self.playerPassword = password
        self.soloRank = 1

    def __repr__(self):
        return '<User %r>' % (self.playerName)

    def getId(self):
        return self.player_id

    def getSoloRank(self):
        return self.soloRank

    def getSoloRankName(self):
        rank = self.soloRank
        if rank is 4:
            return "major"
        if rank is 3:
            return "Triple A"
        if rank is 2:
            return "Double A"
        if rank is 1:
            return "Single A"

    def updateRank(self, point):
        if point >= 50:
            self.soloRank = 4
        if point >= 35:
            self.soloRank = 3
        if point >= 20:
            self.soloRank = 2
        else :
            self.soloRank = 1

