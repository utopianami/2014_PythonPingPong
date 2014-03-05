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

    totalWin = db.Column(db.Integer)
    totalLose = db.Column(db.Integer)
    totalPoint = db.Column(db.Integer)

    def __init__(self, playerName, password):
        self.playerName = playerName
        self.playerPassword = password
        self.soloRank = 1
        self.minusMaginot = 0
        self.totalWin = 0
        self.totalLose = 0
        self.totalPoint = 0

    def __repr__(self):
        return '<User %r>' % (self.playerName)

    def getId(self):
        return self.player_id

    def getSoloRank(self):
        return self.soloRank

    def getPlayerName(self):
        return self.playerName

    def plusTotalPoint(self, point):
        self.totalPoint += point
        self.updateRank()

    def getSoloRankName(self):
        rank = self.soloRank
        if rank is 4:
            return "Major"
        if rank is 3:
            return "AAA"
        if rank is 2:
            return "AA"
        if rank is 1:
            return "A"

    def updateRank(self):
        if self.totalPoint >= 50:
            self.soloRank = 4
        elif self.totalPoint >= 30:
            self.soloRank = 3
        elif self.totalPoint >= 15:
            self.soloRank = 2
        else :
            self.soloRank = 1
            if self.totalPoint <= -10:
                self.minusMaginot = 1
            else:
                self.minusMaginot = 0

