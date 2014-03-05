#-*- coding: utf-8 -*-
from datetime import datetime, date
from app import db

class Result(db.Model):
    __tablename__ = 'resultTable'


    result_id = db.Column(db.Integer, primary_key=True)
    resultDate = db.Column(db.DATETIME)

    winner = db.Column(db.Integer)
    loser = db.Column(db.Integer)
    winPoint = db.Column(db.Integer)
    losePoint = db.Column(db.Integer)
    suggestResult = db.Column(db.Integer)
    isVerified = db.Column(db.Integer)

    def __init__(self, winner, loser):
        self.winner = winner
        self.loser = loser
        self.resultDate = datetime.now()
        self.isVerified = 0
        self.suggestResult = 0

    def setPoint(self, point):
        self.winPoint = point[0]
        self.losePoint = point[1]

    def getOpponent(self, state):
        if state == "lose":
            return self.winner
        else:
            return self.loser

    def getPoint(self, state):
        if state == "win":
            return self.winPoint
        else:
            return self.losePoint

    def offerPoint(self):
        return self.winPoint