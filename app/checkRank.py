from app.players.models import Player
from app.result.models import Result
from operator import itemgetter
from app import app, db



def getWinGame(playerId):
    winResult = Result.query.filter_by(winner = playerId)
    winGames = winResult.count()
    winPoint = 0
    for result in winResult:
        winPoint += result.winPoint
    return [winGames, winPoint]

def getLoseGame(playerId):
    loseResult = Result.query.filter_by(loser = playerId)
    loseGames = loseResult.count()
    losePoint = 0
    for result in loseResult:
        losePoint += result.losePoint
    return [loseGames, losePoint]


def getOpponentDict(dict, table, state):
    for result in table:
        id = result.getOpponent(state)
        point = result.getPoint(state)
        offerPoint = result.offerPoint()
        if id in dict:
            dict[id]["point"] += point
            dict[id][state] += 1
            if state == "lose":
                dict[id]["offerPoint"] += offerPoint

        else:
            dict.update({id:{}})
            dict[id].update({"point" : point})
            if state == "win":
                dict[id].update({"win" : 1})
                dict[id].update({"lose" : 0})
                dict[id].update({"offerPoint" : 0})
            else:
                dict[id].update({"win" : 0})
                dict[id].update({"lose" : 1})
                dict[id].update({"offerPoint" : offerPoint})
    return dict

