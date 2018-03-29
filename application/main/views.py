from datetime import datetime
from flask import render_template, session, redirect, url_for,abort,flash
from flask_login import login_required, current_user
from ..decorator import admin_required
from . import main
from .forms import NameForm,EditProfileForm,EditProfileAdminForm
from .. import db
from ..models import User,Role


@main.route ('/index', methods=['GET', 'POST'])
def index():
    form = NameForm ()
    if form.validate_on_submit ():
        user = User.query.filter (User.username == form.name.data).first ()
        if user is None:
            user = User (username=form.name.data)
            db.session.add (user)
            db.session.commit ()
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        # form.name.data = ''
        return redirect (url_for ('.index'))  # abbreviation of main.submit_page
        # return redirect (url_for ('main.index'))

    return render_template ('index.html', form=form, name=session.get ('name'), known=session.get ('known', False),
                            )


@main.route('/user/<username>')
def user(username):
    user = User.query.filter(User.username == username).first()
    if not user:
        abort(404)
    return render_template('profile/user.html', user=user)

@main.route('/edit-profile',methods=['GET','POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.realname = form.realname.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('Your profile has been updated.')
        return redirect(url_for('.user',username=current_user.username))
    form.realname.data =  current_user.realname
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('profile/edit_profile.html',form=form)


@main.route('/edit-profile/<int:id>',methods=['GET','POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.realname = form.realname.data
        user.location = form.location.data
        user.about_me = form.location.data
        db.session.add(user)
        flash('The profile has been updated.')
        return redirect(url_for('.user',username = user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.realname.data = user.realname
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template ('profile/edit_profile.html', form=form, user=user)



@main.route ('/secret')
@login_required
def secret():
    return 'Only authenticated user are allowed'


@main.route ('/admin')
@login_required
@admin_required
def for_admins_only():
    return "For administrators!"
