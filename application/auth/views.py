from . import auth
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from .forms import LoginForm, RegistrationForm
from ..models import User
from ..email import send_email
from .. import db


@auth.route ('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm ()
    if form.validate_on_submit ():
        user = User.query.filter (User.email == form.email.data).first ()
        print (user)
        if user is not None and user.verify_password (form.password.data):
            login_user (user, remember=form.remember_me.data)
            return redirect (request.args.get ('next') or url_for ('main.index'))
        flash ('Invalid username or password.')

    return render_template ('authentication/login.html', form=form)


@auth.route ('/logout')
def logout():
    logout_user ()
    flash ('You have been logged out.')
    return redirect (url_for ('main.index'))


@auth.route ('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm ()
    if form.validate_on_submit ():
        user = User (email=form.email.data, username=form.username.data, password=form.password.data)
        db.session.add (user)
        db.session.commit ()
        token = user.generate_confirmation_token ()
        send_email (user.email, 'Confirm Your Account', 'authentication/email/confirm', user=user, token=token)
        flash ('A confirmation email has been sent to you by email.')
        return redirect (url_for ('main.index'))
    return render_template ('authentication/register.html', form=form)


@auth.route ('/confirm/<string:token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect (url_for ('main.index'))
    if current_user.confirm_token (token):
        flash ('You have confirmed your account. Thanks!')
    else:
        flash ('The confirmation link is invalid or has expired.')
    return redirect (url_for ('main.index'))

@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token ()
    send_email (current_user.email, 'Confirm Your Account', 'authentication/email/confirm', user=current_user, token=token)
    flash ('A confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('authentication/unconfirmed.html')

@auth.before_app_request
def before_request():
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.endpoint[:5] != 'auth.' \
            and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))

