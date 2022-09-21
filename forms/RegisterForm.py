from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, Length


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3)])
    name = StringField('Name', validators=[DataRequired(), Length(min=3)])
    surname = StringField('Surname', validators=[DataRequired(), Length(min=3)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    age = IntegerField('Age', validators=[DataRequired()])
    gender = SelectField('Gender', choices=['male', 'female'])
    submit = SubmitField('Register')
