from flask import Flask, render_template
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask import request, redirect, session, flash
from flask import url_for
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Message,Mail
import os

app = Flask (__name__)

app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:an19941013@localhost/test'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

app.config['MAIL_SERVER'] = 'smtp.163.com'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'krdk31333455@163.com'
app.config['MAIL_PASSWORD'] = 'zxc123456'

manager = Manager (app)
bootstrap = Bootstrap (app)
moment = Moment (app)

db = SQLAlchemy (app)
mail = Mail(app=app)


@app.route ('/')
def hello_world():
    return render_template ('index.html', current_time=datetime.utcnow ())


@app.route ('/user/<name>')
def user_page(name):
    return render_template ('user.html', name=name)


@app.route ('/test/<name>', endpoint='attempt')
def test(name):
    return url_for ('attempt', name='ject', _external=True)


@app.route ('/submit/page', methods=['GET', 'POST'])
def submit_page():
    form = NameForm ()
    if form.validate_on_submit ():
        user = User.query.filter(User.username == form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        # form.name.data = ''
        return redirect (url_for ('submit_page'))

    return render_template ('submit_page.html', form=form, name=session.get ('name'),known = session.get('known',False))


@app.errorhandler (404)
def page_not_found(e):
    return render_template ('404.html'), 404


class NameForm (FlaskForm):
    name = StringField ("What is your name?", validators=[DataRequired ()])
    submit = SubmitField ('Submit')


class Role (db.Model):
    __tablename__ = 'roles'
    id = db.Column (db.Integer, primary_key=True)
    name = db.Column (db.String (64), unique=True)
    users = db.relationship ('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User (db.Model):
    __tablename__ = 'users'
    id = db.Column (db.Integer, primary_key=True)
    username = db.Column (db.String (64), unique=True, index=True)
    role_id = db.Column (db.Integer, db.ForeignKey ('roles.id'))

    def __repr__(self):
        return '<User % r>' % self.username


def inspect():
    admin_role = Role (name='Admin')
    mod_role = Role (name='Moderator')
    user_role = Role (name='User')
    user_john = User (username='john', role=admin_role)
    user_a = User (username='a', role=user_role)
    user_b = User (username='b', role=user_role)
    db.session.add_all ([admin_role, mod_role, user_role, user_john, user_a, user_b])
    db.session.commit ()

def send_mail():
    msg = Message('Test Subject',sender=app.config.get('MAIL_USERNAME'),recipients=['351264614@qq.com'])
    msg.body = 'text body'
    msg.html = '<b>HTNML</b> body'
    with app.app_context():
        mail.send(msg)

if __name__ == '__main__':
    send_mail()
    # print (Role.query.all ())
    # print (Role.query.filter_by (name='User').first ())
    # print(User.query.filter(Role.name=='User').order_by(User.username.desc()))
    # print(User.query.filter(Role.name=='User',Role.id == User.role_id).order_by(User.username.desc()))
    # print (User.query.filter(Role.name=='User',Role.id == User.role_id).order_by(User.username.desc()).all())

    # inspect()
    # db.create_all ()
    # manager.run()
    # app.run (debug=True)
