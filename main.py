#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from random import randint
import os
import cgi

import jinja2
import webapp2
from google.appengine.ext import ndb
from google.appengine.api import users
from webapp2_extras import json

jinja_environment = jinja2.Environment(autoescape=True,
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__))
)


class Game(ndb.Model):
    name = ndb.StringProperty()
    game_id = ndb.IntegerProperty()
    players = ndb.StringProperty()
    players_max = ndb.IntegerProperty()
    players_current = ndb.IntegerProperty()
    deck = ndb.StringProperty()


class Player(ndb.Model):
    name = ndb.StringProperty()
    player_id = ndb.IntegerProperty()
    tokens = ndb.IntegerProperty()

class Dealer(ndb.Model):
    game_id = ndb.IntegerProperty()
    dealer_cards = ndb.StringProperty()

class GameStatus(ndb.Model):
    game_id = ndb.IntegerProperty()
    name = ndb.StringProperty()
    player_id = ndb.IntegerProperty()
    tokens = ndb.IntegerProperty()
    your_actions = ndb.StringProperty()
    your_cards_visible = ndb.StringProperty()
    common_cards_visible = ndb.StringProperty()
    players = ndb.StringProperty()


class GameHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write('<html><head><title>Black Jack, Son!</title></head><body><h1>Pick a game, yo!</h1>')
        games = ndb.gql("SELECT * FROM Game").fetch()
        self.response.out.write('<input placeholder="username" type="text" id="username">')
        self.response.out.write('<table border = "1"><tr><th>Name</th><th>ID</th><th>Current Players</th><th>Max Players</th><th>Join Game</th></tr>')
        for game in games:
            game_id = game.game_id
            game_name = game.name
            players_max = game.players_max
            players_current = game.players_current
            self.response.out.write(
                "<tr><td>" + str(game_name) + "</td><td>" + str(game_id) + "</td><td>" + str(players_current) + "</td><td>" + str(players_max) + '</td><td><button type="button" class="join" id="' + str(game_id) + '">Join</button></td></tr>')
        self.response.out.write("</table>")
        form = '<form name="myform" action="http://localhost:8080/games" method="POST">Game Name:<input type = "text" name = "name"><input type="submit" value="Create a new game"></form>'
        self.response.out.write(form)
        self.response.out.write('<script src="/js/jquery.min.js" type="text/javascript" ></script>')
        self.response.out.write('<script src="/js/gamepage.js" type="text/javascript" ></script>')
        self.response.out.write('<a href="http://localhost:8080/clear">Clear entire datastore... for debug purposes ONLY!</a>')
        self.response.out.write("</body></html>")

    def post(self):
        #self.response.out.write('Game Handler post')
        #user = users.get_current_user()
        key = randint(0, 999999999)
        game = Game(name=cgi.escape(self.request.get('name')),
                    game_id=key,
                    players=json.encode([]),
                    players_max=6,
                    players_current=0,
                    deck=json.encode(["2h", "3h", "4h", "5h", "6h", "7h", "8h", "9h", "10h", "Jh", "Qh", "Kh", "Ah",
                                      "2d", "3d", "4d", "5d", "6d", "7d", "8d", "9d", "10d", "Jd", "Qd", "Kd", "Ad",
                                      "2s", "3s", "4s", "5s", "6s", "7s", "8s", "9s", "10s", "Js", "Qs", "Ks", "As",
                                      "2c", "3c", "4c", "5c", "6c", "7c", "8c", "9c", "10c", "Jc", "Qc", "Kc", "Ac"]))
        game.put()
        dealer = Dealer(game_id=key,
                        dealer_cards="")
        dealer.put()


class PlayerConnectHandler(webapp2.RequestHandler):
    def post(self):
        #self.response.out.write("Player Connect post")
        game_id = self.request.path
        game_id = game_id.replace('/game/', '')
        game_id = game_id.replace('/playerConnect', '')
        username = str(self.request.get('username'))
        player = ndb.gql("SELECT * FROM Player WHERE name = '" + username + "'").fetch()
        if len(player) == 0:
            key = randint(0, 99999999)
            player = Player(name=username,
                            player_id=key,
                            tokens=1000)
            player.put()
            game_status = GameStatus(game_id=int(game_id),
                                     name=username,
                                     player_id=key,
                                     tokens=1000,
                                     your_cards_visible=json.encode([]),
                                     common_cards_visible=json.encode([]),
                                     your_actions=json.encode([]))
            game_status.put()
        else:
            player = player[0]
            game_status = ndb.gql("SELECT * FROM GameStatus WHERE name = '" + username + "' AND game_id = " + game_id).fetch()
            if len(game_status) == 0:
                game_status = GameStatus(game_id=int(game_id),
                                         name=username,
                                         player_id=player.player_id,
                                         tokens=1000,
                                         your_cards_visible=json.encode([]),
                                         common_cards_visible=json.encode([]),
                                         your_actions=json.encode([]))
            else:
                game_status = game_status[0]
            game_status.put()
        game_retrieved = ndb.gql("SELECT * FROM Game WHERE game_id = " + game_id).fetch()
        game_retrieved = game_retrieved[0]
        if game_retrieved.players_current == 6:
            self.response.out.write("error")
        else:
            players_array = json.decode(game_retrieved.players)
            check_player = 0
            for p in players_array:
                if p == player.name:
                    check_player = 1
            if check_player == 0:
                players_array.append(player.name)
                game_retrieved.players = json.encode(players_array)
                game_retrieved.players_current += 1
                game_retrieved.put()
            self.response.out.write("ok")


class StatusHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("Status Handler get")


class VisibleTableHandler(webapp2.RequestHandler):
    def get(self):
        username = str(self.request.get('player'))
        player = ndb.gql("SELECT * FROM Player WHERE name = '" + username + "'").fetch()
        player = player[0]
        template_values = {
            'username':  username,
            'tokens': player.tokens
        }
        template = jinja_environment.get_template('table.html')
        self.response.out.write(template.render(template_values))


class ActionHandler(webapp2.RequestHandler):
    def post(self):
        username = str(self.request.get('player'))
        player = ndb.gql("SELECT * FROM Player WHERE name = '" + username + "'").fetch()
        player = player[0]
        game_status = ndb.gql("SELECT * FROM GameStatus WHERE name = '" + username + "'").fetch()
        game_status = game_status[0]
        action = str(self.request.get('action'))
        if action == "bet":
            value = int(self.request.get('value'))
            if value > player.tokens:
                self.response.out.write("Bet more than the number of tokens you have")
            else:
                player.tokens -= value
                game_status.tokens -= value
                actions_array = json.decode(game_status.your_actions)
                actions_array.append("bet")
                game_status.your_actions = json.encode(actions_array)
                player.put()
                game_status.put()
                self.response.out.write("ok")
        elif action == "play":
            blah = 1
        # elif action == "draw":
        #
        # elif action == "fold":
        #
        # elif action == "doubledown":

        else:
            self.response.out.write("error")

class ClearHandler(webapp2.RequestHandler):
    def get(self):
        self.deleteAll()

    def post(self):
        self.deleteAll()

    def deleteAll(self):
        self.deleteKeys(ndb.gql('SELECT * FROM Player').fetch())
        self.deleteKeys(ndb.gql('SELECT * FROM GameStatus').fetch())
        self.deleteKeys(ndb.gql('SELECT * FROM Game').fetch())
        self.response.out.write("Datastore has been successfully cleared!!!")

    def deleteKeys(self, keys):
        for key in keys:
            key.key.delete()


app = webapp2.WSGIApplication([('/games', GameHandler),
                               ('/game/.*/playerConnect', PlayerConnectHandler),
                               ('/game/.*/visible_table', VisibleTableHandler),
                               ('/game/.*/action', ActionHandler),
                               ('/game/.*/status', StatusHandler),
                               ('/clear', ClearHandler)
                              ], debug=True)