from datetime import datetime
from app import db

class Result(db.Model):
    __tablename__ = 'resultTable'


    result_id = db.Column(db.Integer, primary_key=True)
    resultDate = db.Column(db.DateTime)

    winner = db.Column(db.Integer)
    loser = db.Column(db.Integer)
    winPoint = db.Column(db.Integer)
    losePoint = db.Column(db.Integer)
    winnerGetSet = db.Column(db.Integer)
    loserGetSet = db.Column(db.Integer)


    def __init__(self, winner, loser, winnerGetSet, loserGetSet):
        self.winner = winner
        self.loser = loser
        self.winnerGetSet = winnerGetSet
        self.loserGetSet = loserGetSet
        self.resultDate = datetime.now()

    def setPoint(self, point):
        self.winPoint = point[0]
        self.loserPoint = point[1]