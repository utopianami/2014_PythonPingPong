from flask import Blueprint, request, render_template, session, redirect, url_for, json
from app.result.models import Result
from app.players.models import Player
from app import db

mod = Blueprint('result', __name__, url_prefix='/result')

@mod.route('/')
def result():
    dbInPlayers = Player.query.all()
    ############################
    session['player_id'] = 1 #test
    ############################

    self = Player.query.filter_by(player_id = session['player_id']).first()
    dbInPlayers.remove(self)
    selfName = self.playerName

    playerList = [dict(id = players.player_id, name = players.playerName) for players in dbInPlayers]

    return render_template('result_register.html', name = selfName, playerList=playerList)

@mod.route('/save', methods=['GET'])
def saveResult():
    player1Set = request.args.get('player1Set')
    player2Set = request.args.get('player2Set')
    ############################
    session['player_id'] = 1
    ############################

    player1 = Player.query.filter_by(player_id = session['player_id']).first()
    player2 = Player.query.filter_by(player_id = request.args.get('player2_id')).first()

    if player1Set > player2Set:
        result = Result(player1.getId(), player2.getId(), player1Set, player2Set)
        point = setRankPoint(player1, player2)
    else:
        result = Result(player2.getId(), player1.getId(), player2Set, player1Set)
        point = setRankPoint(player2, player1)

    result.setPoint(point)
    db.session.add(result)
    db.session.commit()

    return "d"

def setRankPoint(winner, loser):
    playerGap = winner.getSoloRank() - loser.getSoloRank()
    point = checkRankPoint(playerGap, loser)
    return point

def checkRankPoint(playerGap, loser):
    win = 0
    lose = 1
    rankPoint = {-3:[6, 0], -2:[5, 0], -1:[4, -1], 0:[3, -2],
                 1:[2, -3], 2:[1, -4], 3:[1, -5]}
    winnerPoint = rankPoint[playerGap][win]
    loserPoint = rankPoint[-playerGap][lose]

    if loser.getSoloRank() == 1:
        loserPoint = 0
    point = [winnerPoint, loserPoint]
    return point

