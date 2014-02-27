from flask import Blueprint, request, render_template, session, redirect, url_for
from flask.ext.login import LoginManager, logout_user, login_required
from app import db, app
from app.players.models import Player

mod = Blueprint('players', __name__, url_prefix='/players')
login_manager = LoginManager()
login_manager.init_app(app)

@mod.route('/signUp')
def signUp():
    return render_template('signUp.html')

@mod.route('/register', methods=["POST"])
def register():
    if request.method == "POST":
        isExist = Player.query.filter_by(playerName = request.form['playerName']).first()
        if isExist is not None:
            return 'exist'
        else:
            newPlayer = Player(request.form['playerName'], request.form['playerPassword'])
            db.session.add(newPlayer)
            db.session.commit()
    session['player_id'] = newPlayer.getId()
    return redirect(url_for('index'))

@mod.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        playerName = request.form['playerName']
        password = request.form['playerPassword']
        player = Player.query.filter_by(playerName = playerName).first()
        print playerName
        print password
        print player.playerName

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