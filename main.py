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

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__))
)


class Game(ndb.Model):
    name = ndb.StringProperty()
    game_id = ndb.IntegerProperty()
    players_max = ndb.IntegerProperty()
    players_current = ndb.IntegerProperty()


class Player(ndb.Model):
    name = ndb.StringProperty()
    player_id = ndb.IntegerProperty()
    tokens = ndb.IntegerProperty()


class GameStatus(ndb.Model):
    game_id = ndb.IntegerProperty()
    name = ndb.StringProperty()
    player_id = ndb.IntegerProperty()
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
        self.response.out.write("</body></html>")

    def post(self):
        self.response.out.write('Game Handler post')
        user = users.get_current_user()
        key = randint(0, 999999999)
        game = Game(name = cgi.escape(self.request.get('name')),
                    game_id = key,
                    players_max = 6,
                    players_current = 0)
        game.put()



class PlayerConnectHandler(webapp2.RequestHandler):
    def post(self):
        self.response.out.write("Player Connect post")


class StatusHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("Status Handler get")


class VisibleTableHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("Visible Table Handler get")


class ActionHandler(webapp2.RequestHandler):
    def post(self):
        self.response.out.write("Action Handler Post")


app = webapp2.WSGIApplication([('/games', GameHandler),
                               ('/game/.*/playerConnect', PlayerConnectHandler),
                               ('/game/.*/visible_table', VisibleTableHandler),
                               ('/game/.*/action', ActionHandler),
                               ('/game/.*/status', StatusHandler)
                              ], debug=True)