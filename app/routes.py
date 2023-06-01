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
#THIS IS JUST FOR THE IMAGE AND NAME FOR DREAM TEAM

# @app.route('/dreamteam', methods=["GET", "POST"])
# @login_required
# def dreamteam():
#     form = dream_search()
#     if request.method == "POST":
#         player = form.player.data
#         #THIS URL IS WRONG CHECK API AGAIN
#         url = 'https://stats.nba.com/stats/playoffpicture'
#         response = requests.get(url)
#         if not response.ok:
#             return 'That Player Is Not In The NBA'
        
#         data = response.json()
#         for Player in data:
#             dream_player = {
#                 "image": data["resultSets"]["EastConfPlayoffPicture"]}
#             if not Player.known_player(["name"]):
#                  player = Player()
#                  player.from_dict(dream_player)
#                  player.saveToDB()

#         return render_template('dreamteam.html', form = form, player = dream_player)
#     return render_template('dreamteam.html', form = form)
     

@app.route('/search', methods=["GET", "POST"])
@login_required
def search():
    form = player_search()
    if request.method == "POST":
        player_name = form.player_search.data
        player = Player.query.filter_by(name = player_name).first()
        url = f"https://api-nba-v1.p.rapidapi.com/players/statistics"
        querystring = {"id": player.id, "season": "2022"}
        response = requests.get(url, headers=headers, params=querystring)

        if not response.ok:
                #RETURN OR FLASH MESSAGE
                return 'That Guy Is Not In The NBA Dawg'

        data = response.json()
        #points assists total rebounds
        res = response.json()
        data = res['response']
        print(res)
        points = 0
        assists = 0
        rebounds = 0
        for stats in data:
            points += stats.get("points")
            assists += stats.get("assists")
            rebounds += stats.get("totReb")
        if len(data):
            points /= len(data)
            assists /= len(data)
            rebounds /= len(data)
            

        player_stats = player.to_dict()
        player_stats['points'] = points
        player_stats['assists'] = assists
        player_stats['rebounds'] = rebounds
           
        return render_template('search.html', form = form, player = player_stats)
    return render_template('search.html', form = form)
     

@app.route('/drafts')
@login_required
def show_drafts():
    users = User.query.filter(User.id != current_user.id, User.player).all()
    return render_template('drafts.html', users = users)

# @app.route('/opteam/<id>')
# @login_required
# def opteam(id):
#     user = User.query.filter_by(id = id).first()
#     return render_template('team.html', team = user.pokemon.all(), user = user)
#MAYBE LOTS OF MISPELLED STUFF HERE

#THIS SHOWS MY DRAFT CURRENT USER
@app.route('/mydraft')
@login_required
def my_draft():
    return render_template('mydraft.html', mydraft = current_user.player.all(), user = current_user, player = Player)

@app.route('/diffuser/<id>')
@login_required
def diffuser(id):
    user = User.query.filter_by(id = id).first()
    return render_template('mydraft.html', draft = user.player.all(), user=user)

@app.route('/getplayer/<id>')
@login_required
def get_player(id):
    player = Player.query.filter_by(id = id).first()
    if player in current_user.player:
        flash('That Player Is Already On Your Team Dawg')
        #THIS GOES BACK TO DREAM TEAM BUT YOU DONT HAVE IMAGE YET
        return redirect(url_for('dreamteam'))
    elif current_user.player.count() == 5:
        flash('We Got The Starters You Sitting The Bench')
        return render_template('mydraft.html')
    else:
        flash('Baller Has Been Drafted By You!')
        current_user.player.append(player)
        db.session.commit()
        return render_template('mydraft.html', player = player, user = current_user)

@app.route('/test')
def addplayers():

    url = "https://api-nba-v1.p.rapidapi.com/players"

    querystring = {"country" : "USA"}

    headers = {
        "X-RapidAPI-Key": "ff9aebdf16msh7d7fbeee140d529p11077djsn245b75903513",
        "X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    data = (response.json())['response']

    for player in data:
        player_dict = {
            "name": player["firstname"] + ' ' + player["lastname"],
            "id" : player["id"],
            "birthdate" : player["birth"]["date"],
            "country": player["birth"]["country"],
            "position": player["leagues"]["standard",{}]["pos"],
            "height": f"{player['height']['feets']} ' {player['height']['inches']}  \" ",
            "weight": player["weight"]["pounds"],
            "jersey": player["leagues"].get("standard",{}).get("jersey")
        }
        p = Player()
        p.from_dict(player_dict)

        p.saveToDB()

    p.commitToDB()
