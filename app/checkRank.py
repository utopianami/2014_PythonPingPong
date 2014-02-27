from app.players.models import Player
from app.result.models import Result
from operator import itemgetter



class AllPlayer():
    no = None
    rank = None
    name = None
    win = None
    lose = None
    Point = None

    def __init__(self, name ):
        self.name = name

def getInfo():
    players = Player.query.all()
    jsonPlayers = []
    for player in players:
        tmpPlayer =AllPlayer(player.playerName)

        win= getWinGame(player.player_id)
        lose = getWinGame(player.player_id)
        tmpPlayer.win = win[0]
        tmpPlayer.lose= lose[0]
        tmpPlayer.point= win[1] + lose[0]
        jsonPlayers.append(tmpPlayer)
    sortedPlayer = sorted(jsonPlayers, key=itemgetter('Point'))

    return sortedPlayer

def getWinGame(playerId):
    winResult = Result.query.filter_by(winner = playerId)
    winGames =winResult.count()
    winPoint = 0
    for result in winResult:
        winPoint += result.winPoint

    return [winGames, winPoint]

def getLoseGame(playerId):
    loseResult = Result.query.filter_by(loser = playerId)
    loseGames = loseResult.count()
    loserPoint = 0
    for result in loseResult:
        loserPoint += result.loserPoint
    return [loseGames, loserPoint]

