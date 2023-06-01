from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


draft = db.Table('draft',
     db.Column('user_id', db.Integer, db.ForeignKey('user.id'), nullable = False),
     db.Column('player_id', db.Integer, db.ForeignKey('player.id'), nullable = False))

class User(db.Model, UserMixin):
     id = db.Column(db.Integer, primary_key=True)
     username = db.Column(db.String(45), nullable = False, unique = True)
     email = db.Column(db.String(100), nullable = False, unique = True)
     password = db.Column(db.String, nullable = False)
     player = db.relationship('Player', secondary = 'draft', lazy = 'dynamic')

     def __init__(self, username, email, password):
          self.username = username
          self.email = email
          self.password = password
          
     def saveToDB(self):
          db.session.add(self)
          db.session.commit()
          
     def deleteFromDB(self):
          db.session.delete(self)
          db.session.commit()


class Player(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     name = db.Column(db.String(40))
     image = db.Column(db.String(100), nullable = True)
     team = db.Column(db.String(50))
     position = db.Column(db.String(2))
     height = db.Column(db.String(20))
     weight = db.Column(db.Integer)
     birthdate = db.Column(db.String)
     country = db.Column(db.String(30))
     jersey = db.Column(db.Integer)
     #     ppg = db.Column(db.Integer, nullable = False)
     #     apg = db.Column(db.Integer, nullable = False)
     #     rpg = db.Column(db.Integer, nullable = False)


     def saveToDB(self):
         db.session.add(self)
         
     def commitToDB(self):
         db.session.commit()

     def deleteFromDB(self):
         db.session.delete(self)
         db.session.commit()


#When you make the route function for this the player_stats will be a dict where the information is held and it will show up on the page

     def from_dict(self, player_stats):
          self.id = player_stats['id'] 
          self.name = player_stats['name']
          self.team = player_stats['team']
          self.position = player_stats['position']
          self.height = player_stats['height']
          self.weight = player_stats['weight']
          self.birthdate = player_stats['birthdate']
          self.country = player_stats['country']
          self.jersey = player_stats['jersey']
     #    self.ppg = player_stats['PPG']
     #    self.apg = player_stats['APG']
     #    self.rpg = player_stats['RPG']

     def to_dict(self):
          return {
               "id": self.id,
               "name": self.name,
               "team": self.team,
               "position": self.position,
               "height": self.height,
               "weight": self.weight,
               "birthdate": self.birthdate,
               "country": self.country,
               "jersery": self.jersey,
               # "image": self.image
          }

def known_player(name):
     return Player.query.filter_by(player = name).first()


         
         
