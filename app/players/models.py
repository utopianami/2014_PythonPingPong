from app import db

class Player(db.Model):
    __tablename__ = 'playerTable'

    id = db.Column(db.Integer, primary_key=True)
    playerName = db.Column(db.String(80), unique=True)
    playerPassword = db.Column(db.String(80))
    soloRank = db.Column(db.Integer)
    #soloRank = db.Column(db.Integer, db.ForeignKey('rankTable.id'))
    teamRank = db.Column(db.INTEGER)



    def __init__(self, playerName, password):
        self.playerName = playerName
        self.playerPassword = password

    def __repr__(self):
        return '<User %r>' % (self.userEmail)

    def getId(self):
        return self.id

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
