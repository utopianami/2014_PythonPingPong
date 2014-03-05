from flask import Flask, render_template, jsonify, session
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)


from checkRank import *
from app.result.views import checkVerified

@app.route('/')
def index():
    if "player_id" in session:
        playerId = session["player_id"]
        notVerifiedList =checkVerified(playerId)
    else:
        notVerifiedList =[[],[]]

    allPlayer = Player.query.order_by(Player.totalPoint.desc()).all()
    countNo = 1
    playerInfo = []
    for player in allPlayer:
        playerInfo.append(dict(id=player.player_id, no=countNo, rank=player.getSoloRankName(),
                               name=player.playerName, win=player.totalWin, lose=player.totalLose, point=player.totalPoint))
        countNo += 1

    return render_template('main.html', playerInfo = playerInfo, verifiedWin = notVerifiedList[0], verifiedLose = notVerifiedList[1])

from app.players.views import mod as playersModule
from app.result.views import mod as resultModule

app.register_blueprint(resultModule)
app.register_blueprint(playersModule)
