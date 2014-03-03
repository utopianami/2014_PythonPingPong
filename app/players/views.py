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
    if requestName not in studentList & request.form['studentNo'] != studentList[requestName]:
        return "INVALID_SIGNUP_DATA"

    isExist = Player.query.filter_by(playerName = requestName).first()
    if isExist is not None:
        return "INVALID_SIGNUP_DATA"
    else:
        newPlayer = Player(requestName, request.form['playerPassword'])
        db.session.add(newPlayer)
        db.session.commit()
    session['player_id'] = newPlayer.getId()
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

    pushOver = [None, 0]
    revenge = [None, 9999]

    count = 0
    for player in totalDict:
        curPoint = totalDict[player]["point"]
        offerPoint = totalDict[player]["offerPoint"]
        if count == 0:
            pushOver[0] = player
            pushOver[1] = curPoint
            revenge[0] = player
            revenge[1] = offerPoint
            pass
        if offerPoint >= pushOver[1]:
            pushOver[0] = player
            pushOver[1] = offerPoint
        count += 1

    personalPageInfo = {"name" :curPlayer.getPlayerName() , "totalWin" : winTable.count(), "totalLose" : loseTable.count(), "totalRank" :curPlayer.getSoloRankName()}
    if winTable.count() + loseTable.count() < 5:
        return render_template('personal_info.html', personalPageInfo = personalPageInfo, revengeInfo = None, pushOverInfo = None)


    pushOverPlayer = Player.query.filter_by(player_id = pushOver[0]).first()
    revengePlayer = Player.query.filter_by(player_id = revenge[0]).first()
    pushOverInfo = { "player" : pushOverPlayer.getPlayerName(), "win" : totalDict[pushOver[0]]["win"], "lose" : totalDict[pushOver[0]]["lose"], "point" : pushOver[1]}
    revengeInfo = {"player" :revengePlayer.getPlayerName(), "win" : totalDict[revenge[0]]["win"], "lose" : totalDict[revenge[0]]["lose"], "point" : totalDict[revenge[0]]["offerPoint"]}

    return render_template('personal_info.html', personalPageInfo = personalPageInfo, revengeInfo = revengeInfo, pushOverInfo = pushOverInfo)


