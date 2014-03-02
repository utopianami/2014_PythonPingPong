from app.players.models import Player
from app.result.models import Result
from operator import itemgetter



class AllPlayer():
    def __init__(self, name ):
        self.player_id = None
        self.no = None
        self.rank = None
        self.name = name
        self.win = None
        self.lose = None
        self.point = None

def filterPoint(player):
    return player.point

def getInfo():
    players = Player.query.all()
    jsonPlayers = []
    for player in players:
        tmpPlayer = AllPlayer(player.playerName)

        win= getWinGame(player.player_id)
        lose = getLoseGame(player.player_id)

        tmpPlayer.player_id = player.player_id
        tmpPlayer.rank = player.getSoloRankName()
        tmpPlayer.win = win[0]
        tmpPlayer.lose= lose[0]
        tmpPlayer.point= win[1] + lose[1]
        jsonPlayers.append(tmpPlayer)

    sortedPlayer = sorted(jsonPlayers, key=filterPoint, reverse=True)

    return sortedPlayer

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
        if id in dict:
            dict[id]["point"] += point
            dict[id][state] += 1
        else:
            dict.update({id:{}})
            dict[id].update({"point" : 0})
            #윈 루즈 스테이트 확인
            dict[id].update({"win" : 1})
            dict[id].update({"lose" : 1})

    return dict

