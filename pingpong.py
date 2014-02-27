#-*- coding: utf-8 -*-

from app import app, db


db.create_all()


#test case
# from app.players.models import Player
# newPlayer1 = Player("lee", "a")
# newPlayer2 = Player("js", "a")
# newPlayer3 = Player("sh", "a")
#
# db.session.add(newPlayer1)
# #db.session.commit()
# # db.session.add(newPlayer2)
# # # db.session.commit()
# # db.session.add(newPlayer3)
# # db.session.commit()
app.run(debug = True, host='0.0.0.0', port = 7000)