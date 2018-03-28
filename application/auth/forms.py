from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm (Form):
    email = StringField ('Email', validators=[DataRequired (), Length (1, 64), Email ()])
    password = PasswordField ('Password', validators=[DataRequired ()])
    remember_me = BooleanField ('Keep me logged in')
    submit = SubmitField ('Submit')


class RegistrationForm (Form):
    email = StringField ('Email', validators=[DataRequired (), Length (1, 64), Email ()])
    username = StringField ('Username', validators=[DataRequired (), Length (1, 64),
                                                    Regexp ('^[A-Za-z][A-Za-z0-9_.]*$', flags=0,
                                                            message="Usernames must have only letters, 'numbers,dots or underscores'")])
    password = PasswordField('Password',validators=[DataRequired(),EqualTo('password2','Passwords must match.')])
    password2 = PasswordField('Confirm Password',validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_email(self,field):
        if User.query.filter(User.email == field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self,field):
        if User.query.filter(User.username == field.data).first():
            raise ValidationError('Emai already registered.')
