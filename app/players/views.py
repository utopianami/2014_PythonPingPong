#-*- coding: utf-8 -*-

from flask import Blueprint, request, render_template, session, redirect, url_for
from flask.ext.login import LoginManager

from app import db, app
from app.checkRank import *
import studentList


mod = Blueprint('players', __name__, url_prefix='/players')
login_manager = LoginManager()
login_manager.init_app(app)

@mod.route('/signUp')
def signUp():
    return render_template('signUp.html')

@mod.route('/register', methods=["POST"])
def register():
    #checkstudentList
    requestName = request.form['playerName']
    studnetNo = int(request.form['studentNo'])
    requestNameUTF = requestName.encode('utf-8')


    if requestNameUTF not in studentList or studnetNo != studentList[requestNameUTF]:
        return "INVALID_SIGNUP_DATA"

    isExist = Player.query.filter_by(playerName = requestName).first()
    if isExist is not None:
        return "INVALID_SIGNUP_DATA"
    else:
        newPlayer = Player(requestName, request.form['playerPassword'])
        db.session.add(newPlayer)
        db.session.commit()
    session['player_id'] = newPlayer.getId()
    return session['player_id']


@mod.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        playerName = request.form['playerName']
        password = request.form['playerPassword']
        player = Player.query.filter_by(playerName = playerName).first()

        if player == None:
            return "LOGIN_FAIL"
        if player.playerPassword == password:
            session['player_id'] = player.getId()
            return "LOGIN_SUCCESS"

    return "LOGIN_FAIL"

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

    pushOverObject = Player.query.filter_by(player_id = pushOverPlayer).first()
    revengeObject = Player.query.filter_by(player_id = revengePlayer).first()
    pushOverInfo = { "player" : pushOverObject.getPlayerName(), "win" : totalDict[pushOverPlayer]["win"], "lose" : totalDict[pushOverPlayer]["lose"], "point" :  totalDict[pushOverPlayer]["point"]}
    revengeInfo = {"player" :revengeObject.getPlayerName(), "win" : totalDict[revengePlayer]["win"], "lose" : totalDict[revengePlayer]["lose"], "point" : totalDict[revengePlayer]["offerPoint"]}

    if winTable.count() + loseTable.count() < 3:
        return render_template('personal_info.html', personalPageInfo = personalPageInfo, revengeInfo = None, pushOverInfo = None)

    notPushOver = totalDict[pushOverPlayer]["win"] - totalDict[pushOverPlayer]["lose"]
    notRevenge = totalDict[revengePlayer]["win"] - totalDict[revengePlayer]["lose"]

    print "A"
    if notPushOver < 0:
        print pushOverPlayer
        return render_template('personal_info.html', personalPageInfo = personalPageInfo, revengeInfo = revengeInfo, pushOverInfo = None)
    if notRevenge > 0:
        print "c"
        print pushOverPlayer
        return render_template('personal_info.html', personalPageInfo = personalPageInfo, revengeInfo = None, pushOverInfo = pushOverInfo)

    print "B"
    return render_template('personal_info.html', personalPageInfo = personalPageInfo, revengeInfo = revengeInfo, pushOverInfo = pushOverInfo)


