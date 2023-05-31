from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, EqualTo
from flask_wtf import FlaskForm


class player_search(FlaskForm):
    player_search = StringField('Whose stats do you want?: ', validators=[DataRequired()])
    submit = SubmitField('Search')


class dream_search(FlaskForm):
    player_search = StringField('Who In Yo Dream Team Dawg!: ', validators=[DataRequired()])
    submit = SubmitField('Search')
    
