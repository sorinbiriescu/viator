from flask_wtf import FlaskForm
from wtforms import (BooleanField, Form, PasswordField, SelectField,
                     StringField, SubmitField, TextField)
from wtforms.validators import DataRequired, Email

from app.models.models_user import UserRoute


class SearchForm(FlaskForm):
    autocomp = TextField('Search City', id='location-search-autocomplete',render_kw={"type":"search","class":"form-control mr-sm-2","placeholder":"Search city"})

class PoiTypeForm(FlaskForm):
    museum = BooleanField(label='Museum', id='museum-poi-type-checkbox')
    hotel = BooleanField(label='Hotel', id='hotel-poi-type-checkbox')

class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField("Sign In")

class SignupForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField("Sign up")

class RouteForm(FlaskForm):
    route_list = SelectField('Routes', choices=[(1,"Please wait")], coerce=int)
    select_route = SubmitField("Select route")
    new_route = StringField('New route name', validators=[DataRequired()])
