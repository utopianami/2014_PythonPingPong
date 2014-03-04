from app import db
from app.result.models import Result

class Player(db.Model):
    __tablename__ = 'playerTable'

    player_id = db.Column(db.Integer, primary_key=True)
    playerName = db.Column(db.String(80), unique=True)
    playerPassword = db.Column(db.String(80))
    soloRank = db.Column(db.Integer)
    teamRank = db.Column(db.Integer)
    minusMaginot = db.Column(db.Integer)

    def __init__(self, playerName, password):
        self.playerName = playerName
        self.playerPassword = password
        self.soloRank = 1
        self.minusMaginot = 0

    def __repr__(self):
        return '<User %r>' % (self.playerName)

    def getId(self):
        return self.player_id

    def getSoloRank(self):
        return self.soloRank

    def getPlayerName(self):
        return self.playerName

    def getSoloRankName(self):
        rank = self.soloRank
        if rank is 4:
            return "Major"
        if rank is 3:
            return "Triple A"
        if rank is 2:
            return "Double A"
        if rank is 1:
            return "Single A"

    def updateRank(self, point):
        if point >= 50:
            self.soloRank = 4
        elif point >= 30:
            self.soloRank = 3
        elif point >= 15:
            self.soloRank = 2
        else :
            self.soloRank = 1
            if point <= -10:
                self.minusMaginot = 1
        db.session.commit()

