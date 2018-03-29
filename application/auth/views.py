from . import auth
import os
import hashlib
from flask import render_template, redirect, request, url_for, flash,abort,current_app
from flask_login import login_user, logout_user, login_required, current_user
from .forms import LoginForm, RegistrationForm,ChangeEmailForm,PasswordResetForm,ChangeAvatarForm
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


@auth.route ('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token ()
    send_email (current_user.email, 'Confirm Your Account', 'authentication/email/confirm', user=current_user,
                token=token)
    flash ('A confirmation email has been sent to you by email.')
    return redirect (url_for ('main.index'))


@auth.route ('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect (url_for ('main.index'))
    return render_template ('authentication/unconfirmed.html')


@auth.route('/change-email',methods=['GET','POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        current_user.email = form.email.data
        db.session.add(current_user)
        flash('email has been changed')
        return redirect(url_for('main.index'))
    return render_template('authentication/change_email.html',form=form)


@auth.route('/change-password',methods=['GET','POST'])
@login_required
def change_password():
    form = PasswordResetForm()
    if form.validate_on_submit():
        current_user.password = form.password.data
        db.session.add(current_user)
        flash('password has been reset')
        return redirect(url_for('main.index'))
    return render_template('authentication/reset_password.html',form=form)

@auth.route('/change-avatar',methods=['GET','POST'])
@login_required
def change_avatar():
    form = ChangeAvatarForm()
    if form.validate_on_submit():
        image_data = request.files[form.avatar_bin.name].read()
        image_suffix = '.' + form.avatar_bin.data.filename.split('.')[-1]
        image_name = hashlib.md5(str(current_user.id).encode('utf-8')).hexdigest() + image_suffix
        image_path = os.path.join(os.getcwd(),'application/static',current_app.config['AVATAR_STATIC_PATH'],image_name)
        with open(image_path,'wb') as f:
            f.write(image_data)
        current_user.avatar = os.path.join(current_app.config['AVATAR_STATIC_PATH'],image_name)
        db.session.add(current_user)
        flash('avatar has been changed')
        return redirect(url_for('main.index'))
    return render_template('authentication/change_avatar.html',form=form)

@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping ()
        if not current_user.confirmed \
                and request.endpoint[:5] != 'auth.' \
                and request.endpoint != 'static':
            return redirect (url_for ('auth.unconfirmed'))
