from flask import render_template, request, flash, redirect, url_for
from app import app
from forms import player_search
import requests
from .models import User, Player, db, Player_stats
from flask_login import login_required, current_user
#The imports don't work because you need to FLASK DB INIT


@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/search', methods=["GET", "POST"])
@login_required
def search():
    form = player_search()
    if request.method == "POST":
        player_name = form.player_name.data
        #URL check later prob wrong
        url = f'https://nba-stats4.p.rapidapi.com/players/%7Bid%7D{player_name}/'
        response = requests.get(url)
        if not response.ok:
                #Return or FLASH message
                return 'That Guy Is Not In The NBA Dawg'
        
        data = response.json()
        for Player in data:
            Player_stats = {
                 "id":data['id'],
                 "name": data['name'],
                 "image": data['Image'],
                 "team": data['team'],
                 "height": data['height'],
                 "weight": data['weight'],
                 "age": data['age'],
                 "country": data['country'],
                 "ppg": data['PPG'],
                 "apg": data['APG'],
                 "rpg": data['RPG']}
            if not Player.known_player(Player_stats['name']):
                 player = Player()
                 player.from_dict(Player_stats)
                 player.saveToDB()
        return render_template('search.html', form = form, player = Player_stats)
    return render_template('search.html', form = form)
                 
#Add players to your DREAM TEAM
#Show Users to see all other users and display on home page

@app.route('/add/<id>')
@login_required
def add_player(id):
     pass
     
@app.route('/showusers')
@login_required
def users():
     pass
     











    # player = player.filter_by(id = id).first()
    # if player in current_user.dream_team:
    #     flash('Player is already on the team')
    #     # return render_template()
    # elif 



#Make a search function that finds players that shows just image and team and adds onto
#DRAFT TEAM
#Make a similar search function that shows just the stats for the player information

#Make a route that shows the other users draft teams and display on home page
#STATS route for players and (teams)