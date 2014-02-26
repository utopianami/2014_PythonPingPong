from app import db

class Result(db.Model):
    __tablename__ = 'resultTable'


    player_id = db.Column(db.String(80), primary_key=True)
    winner = db.Column(db.Integer)
    loser = db.Column(db.Integer)
    winner = db.Column(db.Integer, db.ForeignKey('playerTable.id'))
    loser = db.Column(db.Integer, db.ForeignKey('playerTable.id'))
    winPoint = db.Column(db.Integer)
    losePoint = db.Column(db.Integer)
    winnerGetSet = db.Column(db.Integer)
    loserGetSet = db.Column(db.Integer)


    def __init__(self, winner, loser, winnerGetSet, loserGetSet):
        self.winner = winner
        self.loser = loser
        self.winnerGetSet = winnerGetSet
        self.loserGetSet = loserGetSet

    def setPoint(self, point):
        self.winPoint = point[0]
        self.loserPoint = point[1]