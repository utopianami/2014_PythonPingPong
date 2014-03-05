#-*- coding: utf-8 -*-
from flask import Blueprint, request, render_template, session, redirect, url_for, json
from app.result.models import Result
from app.players.models import Player
from app import db
from app.checkRank import *
from datetime import datetime, date

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
        point = setRankPoint(player1, player2)
    else:
        result = Result(player2.getId(), player1.getId())
        point = setRankPoint(player2, player1)

    result.suggestResult = session['player_id']
    result.setPoint(point)
    db.session.add(result)
    db.session.commit()

    return redirect(url_for('index'))

def setRankPoint(winner, loser):
    playerGap = winner.getSoloRank() - loser.getSoloRank()
    point = checkRankPoint(playerGap, loser)

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

def checkVerified(playerId):
    winList  = Result.query.filter(Result.winner == playerId, Result.isVerified == 0, Result.suggestResult != session['player_id']).all()
    loseList = Result.query.filter(Result.loser == playerId, Result.isVerified == 0, Result.suggestResult != session['player_id']).all()

    sendVerifiedList = []
    verifiedWin =[]
    verifiedLose = []


    if winList:
        verifiedWin = [dict(result_id = result.result_id, result = "승", opponent = getPlayer(result.loser).playerName,
                            date = transferDate(result.resultDate))for result in winList]
    if loseList:
        verifiedLose = [dict(result_id = result.result_id, result = "패", opponent = getPlayer(result.winner).playerName,
                             date = transferDate(result.resultDate))for result in loseList]


    sendVerifiedList.append(verifiedWin)
    sendVerifiedList.append(verifiedLose)
    return sendVerifiedList

def transferDate(date):
    month = {1:"Jan", 2:"Feb", 3:"Mar", 4:"Apr", 5:"May", 6:"Jun",7:"Jul", 8:"Aug", 9:"Sep", 10:"Oct", 11:"Nov",12:"Dec"}
    transfer = month[date.month]+" "+str(date.day)
    return transfer

def getPlayer(id):
    player = Player.query.filter_by(player_id = id).first()
    return player


@mod.route('/verify', methods=['POST'])
def verify():
    try:
        verifiedId = request.form["result_id"]
        verfiedMessage = int(request.form["status"])
        verifiedResult = Result.query.filter_by(result_id = verifiedId).first()

        if verfiedMessage == 1:
            verifiedResult.isVerified =1
            winner = getPlayer(verifiedResult.winner)
            winner.totalWin += 1
            winner.plusTotalPoint(verifiedResult.winPoint)

            loser = getPlayer(verifiedResult.loser)
            loser.totalLose += 1
            loser.plusTotalPoint(verifiedResult.losePoint)

        if verfiedMessage == 2:
            verifiedResult.isVerified =2

        db.session.commit()
        return "IS_VERIFIED"
    except:
        return "IS_NOT_VERIFIED"