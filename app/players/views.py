from flask import Blueprint, request, render_template, session, redirect, url_for, json
from app import db
from app.players.models import Player

mod = Blueprint('players', __name__, url_prefix='/players')


@mod.route('/signUp')
def signUp():
    return render_template('signUp.html')

@mod.route('/register', methods=['POST'])
def register():
    if (Player.query.filter_by(playerName = request.form['playerName']).first()):
        return 'exist'
    else:
        newPlayer = Player(request.form['playerName'], request.form['playerPassword'])
        db.session.add(newPlayer)
        db.session.commit()

    return redirect(url_for('index'))

@mod.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        playerName = request.form['playerName']
        password = request.form['playerPassword']
        player = Player.query.filter_by(playerName = playerName).first()

        if player == None:
            return 'Wrong'
        if player.playerName == password:
            session['player_id'] = player.getId()
            return redirect(url_for('index'))

    return 'Wrong'

