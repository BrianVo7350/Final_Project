from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin


db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45), nullable = False, unique = True)
    email = db.Column(db.String(100), nullable = False, unique = True)
    password = db.Column(db.String, nullable = False)

    def saveToDB(self):
         db.session.add(self)
         db.session.commit()

    def deleteFromDB(self):
         db.session.delete(self)
         db.session.commit()


class Player(db.model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    image = db.Column(db.String(100), nullable = False)
    team = db.Column(db.String(50))
    height = db.Column(db.String(10)) #OR NUMERIC
    weight = db.Column(db.Integer)
    age = db.Column(db.Integer, nullable = False)
    country = db.Column(db.String(30))
    ppg = db.Column(db.Integer, nullable = False)
    apg = db.Column(db.Integer, nullable = False)
    rpg = db.Column(db.Integer, nullable = False)


    def saveToDB(self):
         db.session.add(self)
         db.session.commit()

    def deleteFromDB(self):
         db.session.delete(self)
         db.session.commit()


#When you make the route function for this the player_stats will be a dict where the information is held and it will show up on the page

    def from_dict(self, player_stats):
        self.id = player_stats['id'] 
        self.name = player_stats['name']
        self.image = player_stats['Image']
        self.team = player_stats['team']
        self.height = player_stats['height']
        self.weight = player_stats['weight']
        self.age = player_stats['age']
        self.country = player_stats['country']
        self.ppg = player_stats['PPG']
        self.apg = player_stats['APG']
        self.rpg = player_stats['RPG']


         
         
