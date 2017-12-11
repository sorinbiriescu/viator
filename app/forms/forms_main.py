from flask_wtf import FlaskForm
from wtforms import (BooleanField, Form, PasswordField, StringField,
                     SubmitField, TextField, SelectField)
from wtforms.validators import DataRequired, Email
from app import UserRoute


class SearchForm(FlaskForm):
    autocomp = TextField('Search City', id='location-search-autocomplete',render_kw={"type":"search","class":"form-control mr-sm-2","placeholder":"Search city"})

class PoiTypeForm(FlaskForm):
    restaurant = BooleanField(label='Restaurants', id='restaurant-poi-type-checkbox')
    bar = BooleanField(label='Bar', id='bar-poi-type-checkbox')
    nightclub = BooleanField(label='Nightclub', id='nightclub-poi-type-checkbox')
    toilets = BooleanField(label='Toilet', id='toilets-poi-type-checkbox')

class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField("Sign In")

class SignupForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField("Sign up")

class Route(FlaskForm):
    route_list = SelectField('Routes', choices=[(1,"Please wait")], coerce=int)
    select_route = SubmitField("Select route")
    new_route = StringField('New route name', validators=[DataRequired()])