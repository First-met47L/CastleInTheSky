from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from . import login_manager


class Role (db.Model):
    __tablename__ = 'roles'
    id = db.Column (db.Integer, primary_key=True)
    name = db.Column (db.String (64), unique=True)
    default = db.Column(db.Boolean,default=False,index=True)
    permissions = db.Column (db.Integer)
    users = db.relationship ('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User (db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column (db.Integer, primary_key=True)
    email = db.Column (db.String (64), unique=True, index=True)
    username = db.Column (db.String (64), unique=True, index=True)
    role_id = db.Column (db.Integer, db.ForeignKey ('roles.id'))
    password_hash = db.Column (db.String (128))
    confirmed = db.Column (db.Boolean, default=False)

    @property
    def password(self):
        raise AttributeError ('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash (password)

    def verify_password(self, password):
        return check_password_hash (self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer (secret_key=current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps ({'confirm': self.id})

    def confirm_token(self, token):
        s = Serializer (secret_key=current_app.config['SECRET_KEY'])
        try:
            data = s.loads (token)
        except Exception:
            return False
        if data.get ('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add (self)
        return True

    def __repr__(self):
        return '<User % r>' % self.username


@login_manager.user_loader
def load_user(user_id):
    '''
    加载用户的回调函数 加载用户的回调函数接收以 Unicode 字符串形式表示的用户标识符。如果能找到用户,这
    个函数必须返回用户对象;否则应该返回 None
    :param user_id:
    :return:
    '''
    return User.query.get (int (user_id))

class Permission(object):
    '''
    Follow users 0b00000001 (0x01) Follow other users
    Comment on posts made by others 0b00000010 (0x02) Comment on articles written by others
    Write articles 0b00000100 (0x04) Write original articles
    Moderate comments made by others 0b00001000 (0x08) Suppress offensive comments made by others
    Administration access
    0b10000000 (0x80) Administrative access to the site
    '''
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLE = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80