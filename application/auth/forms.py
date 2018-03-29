from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,FileField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User
import re


class LoginForm (FlaskForm):
    email = StringField ('Email', validators=[DataRequired (), Length (1, 64), Email ()])
    password = PasswordField ('Password', validators=[DataRequired ()])
    remember_me = BooleanField ('Keep me logged in')
    submit = SubmitField ('Submit')


class RegistrationForm (FlaskForm):
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

class ChangeEmailForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Length(1,64),Email()])
    submit = SubmitField('Submit')

    def validate_email(self,field):
        if User.query.filter(User.email == field.data).first():
            raise ValidationError('Email already registered.')


class PasswordResetForm(FlaskForm):
    password = PasswordField('New Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Reset Password')


class ChangeAvatarForm(FlaskForm):
    avatar_bin = FileField(label='Choose',validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_avatar_bin(self,field):
        if not re.search (r'\s*\.(jpg|jpeg|png)',field.data.filename):
            raise ValidationError("avatar file's suffix should in [jpg,jpeg,png,gif]")
