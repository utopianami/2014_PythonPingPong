#-*- coding: utf-8 -*-

from flask import Blueprint, request, render_template, session, redirect, url_for
from flask.ext.login import LoginManager, logout_user, login_required
from app import db, app
from app.players.models import Player
from app.result.models import Result
from app.checkRank import *
from app.players.studentList import studentList

mod = Blueprint('players', __name__, url_prefix='/players')
login_manager = LoginManager()
login_manager.init_app(app)

@mod.route('/signUp')
def signUp():
    return render_template('signUp.html')

@mod.route('/register', methods=["POST"])
def register():
    #checknextList
    requestName = request.form['playerName']
    studnetNo = request.form['studentNo']

    if requestName not in studentList or studnetNo != studentList[requestName]:
        return "INVALID_SIGNUP_DATA"


    isExist = Player.query.filter_by(requestName = "이영남").first()
    print isExist
    if isExist is not None:
        return "INVALID_SIGNUP_DATA"
    else:
        pass
        #newPlayer = Player(requestName, getDict['playerPassword'])
        #db.session.add(newPlayer)
        #db.session.commit()
    #session['player_id'] = newPlayer.getId()
    return "SIGNUP_SUCCESS"


@mod.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        playerName = request.form['playerName']
        password = request.form['playerPassword']
        player = Player.query.filter_by(playerName = playerName).first()

        if player == None:
            return redirect(url_for('index', loginFail="True"))
        if player.playerPassword == password:
            session['player_id'] = player.getId()
            return redirect(url_for('index'))

    return redirect(url_for('index', loginFail="True"))

@mod.route('/logout')
def logout():
    session.pop('player_id', None)
    return redirect(url_for('index'))


@mod.route('/<id>')
def personal(id):
    winTable = Result.query.filter_by(winner = id)
    loseTable = Result.query.filter_by(loser = id)
    curPlayer = Player.query.filter_by(player_id = id).first()

    dict = {}
    winDict = getOpponentDict(dict, winTable, "win")
    totalDict = getOpponentDict(winDict, loseTable, "lose")

    pushOverPlayer = None
    revengePlayer = None
    pushOverGap = 0
    revengeGap = 0

    count = 0
    for player in totalDict:
        count +=1
        gap = totalDict[player]["win"] - totalDict[player]["lose"]

        if count == 1:
            pushOverGap = gap
            revengeGap = gap
            pushOverPlayer = player
            revengePlayer = player
            pass

        if gap >= pushOverGap:
            pushOverGap = gap
            pushOverPlayer = player
        else:
            if gap <= revengeGap:
                revengeGap = gap
                revengePlayer = player

    personalPageInfo = {"name" :curPlayer.getPlayerName() , "totalWin" : winTable.count(), "totalLose" : loseTable.count(), "totalRank" :curPlayer.getSoloRankName()}
    if winTable.count() + loseTable.count() < 3:
        return render_template('personal_info.html', personalPageInfo = personalPageInfo, revengeInfo = None, pushOverInfo = None)


    pushOverObject = Player.query.filter_by(player_id = pushOverPlayer).first()
    revengeObject = Player.query.filter_by(player_id = revengePlayer).first()
    pushOverInfo = { "player" : pushOverObject.getPlayerName(), "win" : totalDict[pushOverPlayer]["win"], "lose" : totalDict[pushOverPlayer]["lose"], "point" :  totalDict[pushOverPlayer]["point"]}
    revengeInfo = {"player" :revengeObject.getPlayerName(), "win" : totalDict[revengePlayer]["win"], "lose" : totalDict[revengePlayer]["lose"], "point" : totalDict[revengePlayer]["offerPoint"]}

    return render_template('personal_info.html', personalPageInfo = personalPageInfo, revengeInfo = revengeInfo, pushOverInfo = pushOverInfo)


