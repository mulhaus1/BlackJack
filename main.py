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

import jinja2
import webapp2
from google.appengine.ext import ndb
from google.appengine.api import users
from webapp2_extras import json

jinja_environment = jinja2.Environment(
    loader= jinja2.FileSystemLoader(os.path.dirname(__file__))
)

class Game(ndb.Model):
    name = ndb.UserProperty()
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

class GameHandler (webapp2.RequestHandler):
    def get(self):
        self.response.out.write('<html><head><title>Black Jack, Son!</title></head><body><h1>Pick a game, yo!</h1>')
        self.response.out.write("</body></html>")
    def post(self):
        self.response.out.write('Game Handler post')

class PlayerConnectHandler(webapp2.RequestHandler):
    def post(self):
        self.response.out.write("Player Connect post")

class StatusHandler (webapp2.RequestHandler):
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