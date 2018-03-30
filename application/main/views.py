from datetime import datetime
from flask import render_template, session, redirect, url_for,abort,flash
from flask_login import login_required, current_user
from ..decorator import admin_required
from . import main
from .forms import NameForm,EditProfileForm,EditProfileAdminForm,PostForm
from .. import db
from ..models import User,Role,Post


@main.route ('/index', methods=['GET', 'POST'])
def index():
    form = PostForm()
    if form.validate_on_submit ():
        #current_user 是user的轻度包装，获取user对象使用current_user._get_current_object()
        #author 这种被User.relationship指定的必须用original object
        post = Post(body=form.body.data,author=current_user._get_current_object())
        db.session.add(post)
        flash('article has been posted')
        return redirect(url_for('main.index'))
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html',posts=posts,form=form)


@main.route('/user/<username>')
def user(username):
    user = User.query.filter(User.username == username).first()
    if not user:
        abort(404)
    posts = user.posts.order_by(Post.timestamp.desc()).all()
    return render_template('profile/user.html', user=user,posts=posts)

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
