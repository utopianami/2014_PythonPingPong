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
        userName = request.form['playerName']
        password = request.form['playerPassword']
        user = User.query.filter_by(userEmail = userName).first()

        if user == None:
            return 'alertNoId'
        if user.userPassword == password:
            session['player_id'] = user.getId()
            return redirect(url_for('index'))

    return 'alertWrongPassword'

