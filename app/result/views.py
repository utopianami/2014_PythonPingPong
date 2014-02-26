from flask import Blueprint, request, render_template, session, redirect, url_for, json
from app.result.models import Result
from app.players.models import Player
from app import db

mod = Blueprint('result', __name__, url_prefix='/result')


@mod.route('/save', methods=['GET'])
def saveResult():
    player1Score = request.form['player1Score']
    player2Score = request.form['player2Score']

    player1 = Player.query.filter_by(userId = session['user_id']).first()
    player2 = Player.query.filter_by(userName = request.form['player2Name']).first()

    if player1Score > player2Score:
        result = Result(player1.getId(), player2.getId(), player1Score, player2Score)
        point = setRankPoint(player1, player2)
    else:
        result = Result(player2.getId(), player1.getId(), player2Score, player1Score)
        point = setRankPoint(player2, player1)

    result.setPoint(point)
    db.session.add(result)
    db.session.commit()

    return None

def setRankPoint(winner, loser):
    playerGap = winner.getRank() - loser.getRank()
    point = checkRankPoint(playerGap)
    return point

def checkRankPoint(playerGap):
    win = 0
    lose = 1
    rankPoint = {-3:[6, 0], -2:[5, 0], -1:[4, -1], 0:[3, -2],
                 1:[2, -3], 2:[1, -4], 3:[1, -5]}
    winnerPoint = rankPoint[playerGap][win]
    loserPoint = rankPoint[-playerGap][lose]
    point = [winnerPoint, loserPoint]

    return point

