from flask import Flask, render_template, jsonify
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

from checkRank import *
@app.route('/')
def index():
    jsonPlayers = getInfo()
    playerInfo = [dict(no = player.no , rank = player.rank, name = player.name, win = player.win, lose = player.lose, point = player.point) for player in jsonPlayers ]
    return render_template('main.html', playerInfo = playerInfo)



from app.players.views import mod as playersModule
from app.rank.views import mod as rankModule
from app.result.views import mod as resultModule

app.register_blueprint(rankModule)
app.register_blueprint(resultModule)
app.register_blueprint(playersModule)
