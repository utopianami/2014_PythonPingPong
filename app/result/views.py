from flask import Blueprint, request, render_template, session, redirect, url_for, json
from app.result.models import Result
from app.players.models import Player
from app import db
from app.checkRank import *

mod = Blueprint('result', __name__, url_prefix='/result')

@mod.route('/')
def result():
    dbInPlayers = Player.query.all()

    self = Player.query.filter_by(player_id = session['player_id']).first()
    dbInPlayers.remove(self)
    selfName = self.playerName
    playerList = [dict(id = players.player_id, name = players.playerName) for players in dbInPlayers]

    return render_template('result_register.html', name = selfName, playerList=playerList)

@mod.route('/save', methods=['GET'])
def saveResult():
    gameResult = request.args.get('gameResult')

    player1 = Player.query.filter_by(player_id = session['player_id']).first()
    player2 = Player.query.filter_by(player_id = request.args.get('player2_id')).first()

    if gameResult == "win":
        result = Result(player1.getId(), player2.getId())
        point = setRankPoint(player1, player2, result)
    else:
        result = Result(player2.getId(), player1.getId())
        point = setRankPoint(player2, player1, result)


    return redirect(url_for('index'))

def setRankPoint(winner, loser, result):
    playerGap = winner.getSoloRank() - loser.getSoloRank()
    point = checkRankPoint(playerGap, loser)

    winner.totalWin += 1
    winner.plusTotalPoint(point[0])
    loser.totalLose += 1
    loser.plusTotalPoint(point[1])

    try:
        result.setPoint(point)
        db.session.add(result)
        db.session.commit()
    except:
        db.session.rollback()

    return point

def checkRankPoint(playerGap, loser):
    bonusPoint = {-3:[6, 0], -2:[5, 0], -1:[4, -1], 0:[3, -2],
                 1:[2, -3], 2:[1, -4], 3:[1, -5]}
    winnerPoint = bonusPoint[playerGap][0]
    loserPoint = bonusPoint[-playerGap][1]

    if loser.minusMaginot == 1:
        loserPoint = 0
    point = [winnerPoint, loserPoint]

    return point
