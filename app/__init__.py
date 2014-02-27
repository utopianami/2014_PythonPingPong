from flask import Flask, render_template, jsonify
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template('main.html')

####test html
#@app.route('/url')
#def index():
 #   return render_template('main.html')

from app.players.views import mod as playersModule
from app.rank.views import mod as rankModule
from app.result.views import mod as resultModule

app.register_blueprint(rankModule)
app.register_blueprint(resultModule)
app.register_blueprint(playersModule)
