from flask import render_template, request, flash, redirect, url_for
from app import app
from forms import player_search, dream_search
import requests
from .models import User, Player, db
from flask_login import login_required, current_user
#The imports don't work because you need to FLASK DB INIT


@app.route('/')
def home_page():
    return render_template('index.html')

headers = {
	"X-RapidAPI-Key": "ff9aebdf16msh7d7fbeee140d529p11077djsn245b75903513",
	"X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com"
}
querystring =  {"id":"1"}

@app.route('/dreamteam', methods=["GET", "POST"])
@login_required
def dreamteam():
    form = dream_search()
    if request.method == "POST":
        player = form.player.data
        #THIS URL IS WRONG CHECK API AGAIN
        url = f"https://api-nba-v1.p.rapidapi.com/players/{player}/"
        response = requests.get(url, headers=headers, params=querystring)
        if not response.ok:
            return 'That Player Is Not In The NBA'
        
        data = response.json()
        for Player in data:
            dream_player = {
                "image": data["image"]}
            if not Player.known_player(["name"]):
                 player = Player()
                 player.from_dict(dream_player)
                 player.saveToDB()
        return render_template('dreamteam.html', form = form, player = dream_player)
    return render_template('dreamteam.html', form = form)
     
            
                    
          

@app.route('/search', methods=["GET", "POST"])
@login_required
def search():
    form = player_search()
    if request.method == "POST":
        player_name = form.player_name.data
         #THIS URL IS WRONG CHECK API AGAIN
        url = f'https://nba-stats4.p.rapidapi.com/players/%7Bid%7D{player_name}/'
        response = requests.get(url)
        if not response.ok:
                #RETURN OR FLASH MESSAGE
                return 'That Guy Is Not In The NBA Dawg'
        
        data = response.json()
        for Player in data:
            Player_stats = {
                 "id":data["id"],
                 "name": data["name"],
                 "image": data["Image"],
                 "team": data["team"],
                 "height": data["height"],
                 "weight": data["weight"],
                 "age": data["age"],
                 "country": data["country"],
                 "ppg": data["PPG"],
                 "apg": data["APG"],
                 "rpg": data["RPG"]}
            if not Player.known_player(Player_stats["name"]):
                 player = Player()
                 player.from_dict(Player_stats)
                 player.saveToDB()
        return render_template('search.html', form = form, player = Player_stats)
    return render_template('search.html', form = form)
     



# @app.route('/showusers')
# @login_required
# def users():
#      pass




#Make a search function that finds players that shows just image and team and adds onto
#DRAFT TEAM
#Make a similar search function that shows just the stats for the player information

#Make a route that shows the other users draft teams and display on home page
#STATS route for players and (teams)